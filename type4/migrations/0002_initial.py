# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Card'
        db.create_table(u'type4_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_sorcery', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_wrath', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_burn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_lifegain', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_fat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_counterspell', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_masticore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_draw', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'type4', ['Card'])

        # Adding model 'Status'
        db.create_table(u'type4_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['type4.Card'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'type4', ['Status'])


    def backwards(self, orm):
        # Deleting model 'Card'
        db.delete_table(u'type4_card')

        # Deleting model 'Status'
        db.delete_table(u'type4_status')


    models = {
        u'type4.card': {
            'Meta': {'object_name': 'Card'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_burn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_counterspell': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_fat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_lifegain': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_masticore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sorcery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_wrath': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'type4.status': {
            'Meta': {'object_name': 'Status'},
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['type4.Card']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['type4']