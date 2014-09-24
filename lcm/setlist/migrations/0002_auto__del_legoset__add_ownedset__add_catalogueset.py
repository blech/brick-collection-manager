# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LegoSet'
        db.delete_table(u'setlist_legoset')

        # Adding model 'OwnedSet'
        db.create_table(u'setlist_ownedset', (
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
        db.send_create_signal(u'setlist', ['OwnedSet'])

        # Adding model 'CatalogueSet'
        db.create_table(u'setlist_catalogueset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('setID', self.gf('django.db.models.fields.IntegerField')()),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('numberVariant', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('setName', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('subtheme', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('pieces', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('minifigs', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('image', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('imageFilename', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('thumbnailURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('imageURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('bricksetURL', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('own', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('want', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('qtyOwned', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('userNotes', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('UKRetailPrice', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('USRetailPrice', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('CARetailPrice', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('instructionsAvailable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('EAN', self.gf('django.db.models.fields.CharField')(default='', max_length=16)),
            ('UPC', self.gf('django.db.models.fields.CharField')(default='', max_length=16)),
            ('lastUpdated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'setlist', ['CatalogueSet'])


    def backwards(self, orm):
        # Adding model 'LegoSet'
        db.create_table(u'setlist_legoset', (
            ('chain', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('additional_price_paid', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('minifigs', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('condition_when_acquired', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('acquired_from', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('condition_now', self.gf('django.db.models.fields.CharField')(max_length=16)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('will_trade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('set_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('parts', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('online', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_acquired', self.gf('django.db.models.fields.DateField')(null=True)),
            ('current_estimated', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subtheme', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('collection_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('price_paid', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('instructions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('box', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('set_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=6, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'setlist', ['LegoSet'])

        # Deleting model 'OwnedSet'
        db.delete_table(u'setlist_ownedset')

        # Deleting model 'CatalogueSet'
        db.delete_table(u'setlist_catalogueset')


    models = {
        u'setlist.catalogueset': {
            'CARetailPrice': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'EAN': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'Meta': {'ordering': "('number', 'numberVariant')", 'object_name': 'CatalogueSet'},
            'UKRetailPrice': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'UPC': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16'}),
            'USRetailPrice': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '6', 'decimal_places': '2'}),
            'bricksetURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'imageFilename': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'imageURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'instructionsAvailable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastUpdated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'minifigs': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'numberVariant': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'own': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pieces': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'qtyOwned': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'setID': ('django.db.models.fields.IntegerField', [], {}),
            'setName': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'subtheme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'thumbnailURL': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'userNotes': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'want': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'setlist.ownedset': {
            'Meta': {'ordering': "('-date_acquired',)", 'object_name': 'OwnedSet'},
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