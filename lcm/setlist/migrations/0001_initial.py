# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LegoSet'
        db.create_table(u'setlist_legoset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('collection_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('set_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('set_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subtheme', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('date_acquired', self.gf('django.db.models.fields.DateField')(null=True)),
            ('acquired_from', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('price_paid', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('additional_price_paid', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('current_estimated', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('condition_when_acquired', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('condition_now', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('parts', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('minifigs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('instructions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('box', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('will_trade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('online', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('chain', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'setlist', ['LegoSet'])


    def backwards(self, orm):
        # Deleting model 'LegoSet'
        db.delete_table(u'setlist_legoset')


    models = {
        u'setlist.legoset': {
            'Meta': {'object_name': 'LegoSet'},
            'acquired_from': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'additional_price_paid': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'box': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chain': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'collection_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'condition_now': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'condition_when_acquired': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'current_estimated': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'date_acquired': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'minifigs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_paid': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'set_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'set_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subtheme': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'will_trade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['setlist']