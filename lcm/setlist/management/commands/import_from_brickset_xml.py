#!/usr/bin/python

import xmltodict
import datetime
import decimal

from django.core.management.base import BaseCommand, CommandError
from lcm.setlist.models import CatalogueSet

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = []

        for xmlpath in args:
            xmlfile = open(xmlpath, 'r')
            xmlstring = xmlfile.read()
            xmlfile.close()

            catalogue_sets = xmltodict.parse(xmlstring)
            for data in catalogue_sets['ArrayOfSetData']['setData']:
                (catalogue_set, created) = CatalogueSet.objects.get_or_create(setID=data['setID'])

                for key in data.keys():
                    if key in data and data[key]:
                        value = data[key]
                        if value == 'false':
                            value = False
                        setattr(catalogue_set, key, value)

                catalogue_set.save()

                print "Saved catalogue_set %s (Brickset ID %s)" % (
                            catalogue_set.set_number(),
                            catalogue_set.setID
                        )

