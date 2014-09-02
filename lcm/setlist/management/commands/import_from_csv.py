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
from lcm.setlist.models import LegoSet

class Command(BaseCommand):
    def handle(self, *args, **options):
        data = []

        csvfile = open('brickset-acm-20140829.csv', 'r')
        csvreader = csv.reader(csvfile)

        columns = csvreader.next()

        for row in csvreader:
            if not row:
                continue

            (rowdict, set) = self.parse_acm_csv_row(columns, row)
            # set = self.row_to_set(rowdict)

### ACM parser

    def parse_acm_csv_row(self, columns, row):
        truerow = [x if x != "Yes" else True for x in row]

        rowdict = dict(zip(columns, truerow))
        del(rowdict[''])

        collection_id = rowdict.get('CollectionID', None)
        (lego_set, created) = LegoSet.objects.get_or_create(collection_id=collection_id)

        ### set standard attributes
        for key in rowdict:
            field = "_".join(l.lower() for l in re.findall('[A-Z][^A-Z]*', key))
            if field == 'collection_i_d':
                field = 'collection_id'

            setattr(lego_set, field, rowdict[key])

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

    def row_to_set(self, rowdict):
        collection_id = rowdict.get('CollectionID', None)
        (lego_set, created) = LegoSet.objects.get_or_create(collection_id=collection_id)

        for key in rowdict:
            field = "_".join(l.lower() for l in re.findall('[A-Z][^A-Z]*', key))
            if field == 'collection_i_d':
                field = 'collection_id'

            # these get swapped around
            if key == 'DateAcquired':
                continue

            if key == 'Date':
                field = 'date_acquired'
                # print "Using '%s' for date_acquired" % rowdict['Date']

            # print "key %s field %s value %s" % (key, field, rowdict[key])

            setattr(lego_set, field, rowdict[key])

        if not lego_set.price_paid_dec:
            lego_set.price_paid_dec = decimal.Decimal('0.00')
        if not lego_set.additional_price_paid_dec:
            lego_set.additional_price_paid_dec = decimal.Decimal('0.00')
        if not lego_set.current_estimated_value:
            lego_set.current_estimated_value = decimal.Decimal('0.00')
        if not lego_set.date_acquired:
            print "this? %s" % rowdict['CollectionID']

        try:
            lego_set.save()
            print "Saved set Brickset ID %s with our id %s" % (lego_set.collection_id, lego_set.id)
        except Exception, e:
            print "Could not save Brickset ID %s (set %s): %s" % (rowdict['CollectionID'], rowdict['SetNumber'], e)

    ### data manipulation

    def get_totals(data):
        totals = dict()

        totals['owned'] = len(data)
        totals['distinct'] = len(set([x['SetNumber'] for x in data]))

        totals['paid'] = sum([x['PricePaidDec'] for x in data])
        totals['additional'] = sum([x['AdditionalPricePaidDec'] for x in data])
        totals['total'] = totals['paid']+totals['additional']

        return totals

    def get_segments(data):
        # TODO DSL/metalanguage for name/condition mapping
        segments = defaultdict(dict)

        new = [x for x in data if not x['Used']]
        segments['new'] = calculate_segment(new)

        used = [x for x in data if x['Used']]
        segments['used'] = calculate_segment(used)

        online = [x for x in data if x['Online']]
        segments['online'] = calculate_segment(online)

        shop = [x for x in data if not x['Online']]
        segments['shop'] = calculate_segment(shop)

        return segments

    def calculate_segment(set_list):
        detail = dict()

        detail['sets'] = set_list
        detail['count'] = len(set_list)
        detail['cost'] = sum(x['PriceTotal'] for x in set_list)

        return detail

    def get_vendor_details(data):
        vendor_list = set([x['Chain'] for x in data])
        vendors = defaultdict(dict)

        for vendor in vendor_list:
            vendor_sets = [x for x in data if x['Chain'] == vendor]

            vendors[vendor]['sets'] = vendor_sets
            vendors[vendor]['total'] = sum([x['PriceTotal'] for x in vendor_sets])

            # print "    %s: %s sets costing $%s" % (vendor, len(vendor_sets), vendor_total)

            branches = set([x['AcquiredFrom'] for x in vendor_sets])
            if len(branches) > 1:
                vendors[vendor]['branches'] = dict()
                for branch in branches:
                    branch_sets = [x for x in vendor_sets if x['AcquiredFrom'] == branch]

                    vendors[vendor]['branches']['sets'] = branch_sets
                    vendors[vendor]['branches']['total'] = sum([x['PriceTotal'] for x in branch_sets])

        return vendors

    def get_month_details(data):
        months = defaultdict(dict)

        months_text = sorted(set(['%4i/%02i' % (x['Date'].year, x['Date'].month) for x in data if 'Date' in x]))
        months_tuples = sorted(set([(x['Date'].year, x['Date'].month) for x in data if 'Date' in x]))

        months_list = dict(zip(months_text, months_tuples))

        # print "\nBought over %s months" % len(months)

        for month in sorted(months_list):
            month_sets = [x for x in data if 'Date' in x and 
                             x['Date'].year == months_list[month][0] and 
                             x['Date'].month == months_list[month][1]    ]

            months[month]['sets'] = month_sets
            months[month]['count'] = len(month_sets)
            months[month]['cost'] = sum([x['PriceTotal'] for x in month_sets])

        return months

    ### set information
    def get_inventories(data):
        set_list = set([x['SetNumber'] for x in data])

        if not os.path.exists('inventories'):
            os.makedirs('inventories')

        for set_number in sorted(set_list):
            if not os.path.exists('inventories/%s.csv' % set_number):
                fetch_inventory_csv(set_number)

        sys.exit()

    def fetch_inventory_csv(set_number):
        inventory_url = "http://brickset.com/exportscripts/inventory/%s" % set_number
        inventory_file = "inventories/%s.csv" % set_number

        # naughty
        i_am_ie = { 'User-agent' : "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)" }

        req = urllib2.Request(inventory_url, headers=i_am_ie)
        resp = urllib2.urlopen(req)
        with open(inventory_file, "wb") as local_file:
            local_file.write(resp.read())

        print "Fetched %s.csv" % set_number

    ### output

    def report(data):
        totals = get_totals(data)
        months = get_month_details(data)

        print "Have %s sets" % totals['owned']
        print "Have %s different sets" % totals['distinct']
        print "Total cost $%s + $%s (total $%s)" % (totals['paid'], totals['additional'], totals['total'])

        vendors = get_vendor_details(data)

        print "\nFrom %s vendors:" % len(vendors)    
        for vendor in sorted(vendor.keys()):
            print vendor

        # TODO reinstate months (years?)

        segments = get_segments(data)

        print "\n%s sets new (costing $%s)" % (segment['new']['count'], segment['new']['cost'])

        print "%s sets used (costing $%s)" % (count, cost)

        print "\n%s sets online (costing $%s)" % (count, cost)

        print "%s sets in shops (costing $%s)" % (count, cost)
