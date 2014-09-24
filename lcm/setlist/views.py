from datetime import datetime
from decimal import Decimal

from django.db.models import *
from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import OwnedSet
from .serializers import OwnedSetSerializer, OwnedSetChainSerializer
from .serializers import OwnedSetMonthSerializer, OwnedSetThemeSerializer

TWOPLACES = Decimal(10)**-2

class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        now = datetime.datetime.now()
        this_month = OwnedSet.objects.filter(
                        date_acquired__year=now.year,
                        date_acquired__month=now.month,
                     )
        spent = this_month.aggregate(Sum('total_price'), Avg('total_price'))

        context.update({
            'now': now,
            'this_month': this_month,
            'spent': spent,
            'themes': self.get_themes(this_month),
            'chains': self.get_chains(this_month),
            'misb': self.get_misb(),
        })
        return context

    def get_themes(self, sets):
        grouping = []

        themes = sets.values_list("theme", flat=True)
        themes = sorted(list(set(themes)))

        most = max = Decimal(0)
        most_name = max_name = ""

        for theme in themes:
            ownedsets = sets.filter(theme=theme)
            count = ownedsets.count()
            aggregates = ownedsets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'theme': theme, 'ownedsets': ownedsets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            if aggregates['total_price__sum'] > max:
                max_name = theme
                max = aggregates['total_price__sum']
            if count > most:
                most_name = theme
                most = count

            grouping.append(row)

        return {'grouping': grouping, 
                'max': max_name, 'max_cost': max, 
                'most_count': most, 'most': most_name}

    def get_chains(self, sets):
        grouping = []

        chains = sets.values_list("chain", flat=True)
        chains = sorted(list(set(chains)))

        most = max = Decimal(0)
        most_name = max_name = ""

        for chain in chains:
            ownedsets = sets.filter(chain=chain)
            count = ownedsets.count()
            aggregates = ownedsets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'chain': chain, 'ownedsets': ownedsets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            if aggregates['total_price__sum'] > max:
                max_name = chain
                max = aggregates['total_price__sum']
            if count > most:
                most_name = chain
                most = count

            grouping.append(row)

        return {'grouping': grouping, 
                'max': max_name, 'max_cost': max, 
                'most_count': most, 'most': most_name}

    def get_misb(self):
        misb = OwnedSet.objects.filter(condition_now="MISB")[:8]
        return misb

class dthreeView(TemplateView):
    template_name = "d3.html"


class OwnedSetList(APIView):
    """
    List all Lego sets
    """
    def get(self, request, format=None):
        ownedsets = OwnedSet.objects.all()
        serializer = OwnedSetSerializer(ownedsets, many=True)
        return Response(serializer.data)

class OwnedSetDetail(APIView):
    """
    Retrieve, update or delete a OwnedSet instance.
    """
    def get_object(self, pk):
        try:
            return OwnedSet.objects.get(pk=pk)
        except OwnedSet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        OwnedSet = self.get_object(pk)
        serializer = OwnedSetSerializer(OwnedSet)
        return Response(serializer.data)

class OwnedSetMonth(APIView):
    def get(self, request, format=None):
        grouping = []
        dates = OwnedSet.objects.values_list('date_acquired', flat=True)
        months = set([(date.year, date.month) for date in dates if date != None])
        months = sorted(list(months))

        for (year, month) in months:
            ownedsets = OwnedSet.objects.filter(date_acquired__year=year, date_acquired__month=month)
            # TODO generalise from here to the end
            count = ownedsets.count()
            aggregates = ownedsets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'year': year, 'month': month, 'ownedsets': ownedsets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            grouping.append(row)

        serializer = OwnedSetMonthSerializer(grouping, many=True)
        return Response(serializer.data)

class OwnedSetChain(APIView):
    def get(self, request, format=None):
        grouping = []

        chains = OwnedSet.objects.all().values_list("chain", flat=True)
        chains = sorted(list(set(chains)))

        for chain in chains: 
            ownedsets = OwnedSet.objects.filter(chain=chain)
            count = ownedsets.count()
            aggregates = ownedsets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'chain': chain, 'ownedsets': ownedsets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            grouping.append(row)

        serializer = OwnedSetChainSerializer(grouping, many=True)
        return Response(serializer.data)

class OwnedSetTheme(APIView):
    def get(self, request, format=None):
        grouping = []

        themes = OwnedSet.objects.all().values_list("theme", flat=True)
        themes = sorted(list(set(themes)))

        for theme in themes:
            ownedsets = OwnedSet.objects.filter(theme=theme)
            count = ownedsets.count()
            aggregates = ownedsets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'theme': theme, 'ownedsets': ownedsets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            grouping.append(row)

        serializer = OwnedSetThemeSerializer(grouping, many=True)
        return Response(serializer.data)


