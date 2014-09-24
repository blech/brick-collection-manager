#!/usr/bin/python

import csv
import datetime
import decimal
import json
import os
import re
import sys
import urllib2

from collections import defaultdict
from warnings import warn

from django.core.management.base import BaseCommand, CommandError
from lcm.setlist.models import OwnedSet

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = []

        for csvpath in args:
            csvfile = open(csvpath, 'r')
            csvreader = csv.reader(csvfile)

            columns = csvreader.next()

            for row in csvreader:
                if not row:
                    continue

                (rowdict, set) = self.parse_acm_csv_row(columns, row)

### ACM parser

    def parse_acm_csv_row(self, columns, row):
        truerow = [x if x != "Yes" else True for x in row]

        rowdict = dict(zip(columns, truerow))
        del(rowdict[''])

        collection_id = rowdict.get('CollectionID', None)
        (lego_set, created) = OwnedSet.objects.get_or_create(collection_id=collection_id)

        ### set standard attributes
        for key in rowdict:
            field = "_".join(l.lower() for l in re.findall('[A-Z][^A-Z]*', key))
            if field == 'collection_i_d':
                field = 'collection_id'

            value = rowdict[key]
            if value == " ":
                value = False

            setattr(lego_set, field, value)

        ### parse dates

        try:
            [y,m,d] = [int(x) for x in rowdict['DateAcquired'].split('-')]
        except:
            # if rowdict['DateAcquired'] != '':
            #     warn("Datetime not parsed: '%s'" % rowdict['DateAcquired'])
            [d,m,y] = [None,None,None]
            pass

        try:
            lego_set.date_acquired = datetime.date(day=d, month=m, year=y)
        except:
            # warn("Datetime not valid: %s/%s/%s" % (d, m, y))
            print "Could not parse %s - setting date_acquired to None" % rowdict['DateAcquired']
            lego_set.date_acquired = None
            pass

        # if d and m and y and not 'Date' in rowdict:
        #     try:
        #         rowdict['Date'] = datetime.date(year=d, month=m, day=y)
        #         # print "... valid in reverse format"
        #     except:
        #         warn("Datetime not valid: %s-%s-%s" % (d, m, y))
        #         rowdict['Date'] = datetime.date(year=2011, month=1, day=1)

        ### set up additional fields

        lego_set.online = False
        lego_set.used = False

        AF = rowdict['AcquiredFrom']

        ### parse vendor information to chains / online

        if '(ebay)' in AF.lower() or '(bricklink)' in AF.lower():
            # print "Online/Used vendor '%s'" %    rowdict['AcquiredFrom']
            lego_set.online = True
            lego_set.used = True

            lego_set.chain = AF[AF.index('(')+1:AF.index(')')]
            lego_set.vendor = AF.replace('('+lego_set.chain+')', '')

        if 'online' in AF or AF.endswith('com'):
            # print "Online vendor '%s'" %    rowdict['AcquiredFrom']
            lego_set.online = True

        if not lego_set.used:
            if ' (' in AF:
                lego_set.chain = AF[:AF.index(' (')]
                lego_set.vendor = AF[AF.index('(')+1:AF.index(')')]
            else:
                lego_set.chain = AF
                lego_set.vendor = ''

        ### parse prices

        lego_set.price_paid = decimal.Decimal('0.00')
        lego_set.additional_price_paid = decimal.Decimal('0.00')
        if (rowdict['PricePaid']):
            lego_set.price_paid = decimal.Decimal(rowdict['PricePaid'])
        if (rowdict['AdditionalPricePaid']):
            lego_set.additional_price_paid = decimal.Decimal(rowdict['AdditionalPricePaid'])

        lego_set.total_price = lego_set.price_paid+lego_set.additional_price_paid

        ### save object

        try:
            lego_set.save()
            if created:
                print "Created set Brickset ID %s with our id %s" % (lego_set.collection_id, lego_set.id)
        except Exception, e:
            print "Could not save Brickset ID %s (set %s): %s" % (rowdict['CollectionID'], rowdict['SetNumber'], e)

        return (rowdict, lego_set)


