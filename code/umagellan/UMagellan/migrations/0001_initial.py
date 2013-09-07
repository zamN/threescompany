# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'UMagellan_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('section', self.gf('django.db.models.fields.IntegerField')()),
            ('building', self.gf('django.db.models.fields.TextField')(max_length=3)),
            ('room', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users_courses', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'UMagellan', ['Course'])

        # Adding model 'Route'
        db.create_table(u'UMagellan_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='class_start_location', to=orm['UMagellan.Course'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(related_name='class_end_location', to=orm['UMagellan.Course'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'UMagellan', ['Route'])

        # Adding model 'Spot'
        db.create_table(u'UMagellan_spot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=12)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=12)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users_spots', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'UMagellan', ['Spot'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'UMagellan_course')

        # Deleting model 'Route'
        db.delete_table(u'UMagellan_route')

        # Deleting model 'Spot'
        db.delete_table(u'UMagellan_spot')


    models = {
        u'UMagellan.course': {
            'Meta': {'object_name': 'Course'},
            'building': ('django.db.models.fields.TextField', [], {'max_length': '3'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'room': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users_courses'", 'to': u"orm['auth.User']"})
        },
        u'UMagellan.route': {
            'Meta': {'object_name': 'Route'},
            'end': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'class_end_location'", 'to': u"orm['UMagellan.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'class_start_location'", 'to': u"orm['UMagellan.Course']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'UMagellan.spot': {
            'Meta': {'object_name': 'Spot'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '12'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '12'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users_spots'", 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['UMagellan']