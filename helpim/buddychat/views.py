from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from helpim.buddychat.models import BuddyChatProfile

class ConvMessageForm(forms.Form):
    body = forms.CharField(max_length=4096, widget=forms.Textarea)

class CareworkersForm(forms.Form):
    choices = [('', _('None'))]
    careworkers = User.objects.filter(groups__name='careworkers')
    for user in careworkers:
        choices.append((user.pk, user.username))
    careworker = forms.ChoiceField(choices=choices, required=False)

def welcome(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            """ staff doesn't have a profile - redirect to admin """
            return HttpResponseRedirect(reverse('admin:index'))
        else:
            return HttpResponseRedirect(reverse('buddychat_profile', args=[request.user]))
    else:
        return HttpResponseRedirect(reverse('auth_login'))

@login_required
def profile(request, username):
    client = get_object_or_404(BuddyChatProfile, user__username = username)
    if request.user.has_perm('buddychat.is_coordinator') or (request.user.has_perm('buddychat.is_careworker') and request.user == client.careworker) or request.user == client.user:
        """ we need to make sure requesting user is either
        * the careseeker himself (aka the 'client')
        * the careworker associated with this client
        * a coordinator
        """
        if request.method == "POST":
            form = ConvMessageForm(request.POST)
            if form.is_valid():
                """
                POST var 'conv' decides which conversation we're acting on
                """
                conv = {
                    'careworker': client.careworker_conversation,
                    'coordinator': client.coordinator_conversation,
                    'careworker_coordinator': client.careworker_coordinator_conversation
                    }[request.POST['conv']]

                """
                check whether user is allowed to act on this conversation according to this rules
                * careseeker allowed to post to careworker and coordinator
                * careworker allowed to post to careworker and careworker_coordinator
                * coordinator allowed to post to coordinator and careworker_coordinator
                and set rcpt for email notification
                """
                rcpt = None # rcpt is None for coordinators
                if conv is client.careworker_conversation:
                    if not client.careworker:
                        return HttpResponse(_('Access Denied'))
                    elif request.user == client.user:
                        rcpt = client.careworker
                    elif request.user == client.careworker:
                        rcpt = client.user
                    else:
                        return HttpResponse(_('Access Denied'))
                elif conv is client.coordinator_conversation:
                    if request.user.has_perm('buddychat.is_coordinator'):
                        rcpt = client.user
                    elif request.user != client.user:
                        return HttpResponse(_('Access Denied'))
                elif conv is client.careworker_coordinator_conversation:
                    if request.user.has_perm('buddychat.is_coordinator'):
                        rcpt = client.careworker
                    elif request.user != client.careworker:
                        return HttpResponse(_('Access Denied'))

                conv.messages.create(
                    body = form.cleaned_data['body'],
                    sender = conv.get_or_create_participant(request.user),
                    sender_name = request.user.username,
                    created_at = datetime.now()
                    )
                """
                send email
                """
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)

                subject = _('a message from %s' % request.user.username)
                body = _('%s wrote a message on %s\'s profile:\n\n%s\n\nDon\'t reply to this message directly, reply on this user\'s personal page at http://%s/profile/%s/' % (request.user.username, client.user.username, form.cleaned_data['body'], site, client.user.username))

                if not rcpt is None:
                    rcpt.email_user(subject, body)
                else:
                    coordinators = User.objects.filter(groups__name='coordinators')
                    for user in coordinators:
                        user.email_user(subject, body)

                messages.success(request, _('Your message has been sent'))
                form = ConvMessageForm() # reset form
        else:
            form = ConvMessageForm()
        params = {'client': client,
                  'form': form}
        if request.user.has_perm('buddychat.is_coordinator'):
            if client.careworker:
                params['careworkers_form'] = CareworkersForm(initial={'careworker': client.careworker.pk})
            else:
                params['careworkers_form'] = CareworkersForm()

        return render_to_response(
            'buddychat/profile.html',
            params,
            context_instance=RequestContext(request)
            )
    else:
        return HttpResponse(_('Access Denied'))

@permission_required('buddychat.is_coordinator')
def set_cw(request, username):
    """ set a careworker """
    client = get_object_or_404(BuddyChatProfile, user__username = username)
    if request.method == "POST":
        form = CareworkersForm(request.POST)
        if form.is_valid():
            try:
                careworker = User.objects.get(pk=form.cleaned_data['careworker'])
            except ValueError:
                careworker = None
            except User.DoesNotExist:
                careworker = None
                messages.info(request, _('Careworker not found'))
            client.careworker = careworker
            client.save()
            if careworker is None:
                messages.success(request, _('Careworker has been unset'))
            else:
                messages.success(request, _('Careworker has been set'))

    return HttpResponseRedirect(reverse('buddychat_profile', args=[username]))
