from datetime import datetime

from django.contrib import admin

from helpim.buddychat.models import BuddyChatProfile

class BuddyChatProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('user', 'activation_key', 'ready', 'careworker', 'coupled_at')
            }),
        )

    list_display = ('user', 'ready', 'careworker', 'coupled_at', 'personal_page')
    list_filter = ('ready', 'careworker')
    list_editable = ('careworker',)
    readonly_fields = ('user', 'ready', 'activation_key', 'coupled_at')

    def personal_page(self, obj):
        return '<a href="/profile/%s/">View</a>' % obj.user.username
    personal_page.short_description = 'Personal Page'
    personal_page.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        if change and 'careworker' in form.changed_data:
            if obj.careworker is None:
                obj.coupled_at = None
            else:
                obj.coupled_at = datetime.now()
            obj.save()
            
admin.site.register(BuddyChatProfile, BuddyChatProfileAdmin)
