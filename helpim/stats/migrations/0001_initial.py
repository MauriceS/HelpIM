# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Report'
        db.create_table('stats_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('period_start', self.gf('django.db.models.fields.DateField')()),
            ('period_end', self.gf('django.db.models.fields.DateField')()),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.BranchOffice'])),
            ('careworker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('filter_none', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_business_hours', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_blocked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_queued', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_assigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_interactive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('variable1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('variable2', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('output', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('stats', ['Report'])


    def backwards(self, orm):
        
        # Deleting model 'Report'
        db.delete_table('stats_report')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'common.branchoffice': {
            'Meta': {'object_name': 'BranchOffice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stats.report': {
            'Meta': {'object_name': 'Report'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.BranchOffice']"}),
            'careworker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'filter_assigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_business_hours': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_interactive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_none': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_queued': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'output': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'period_end': ('django.db.models.fields.DateField', [], {}),
            'period_start': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variable1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variable2': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['stats']