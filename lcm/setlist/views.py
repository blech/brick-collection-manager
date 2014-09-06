from decimal import Decimal

from django.db.models import *
from django.http import Http404
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LegoSet
from .serializers import LegoSetSerializer, LegoSetMonthSerializer, LegoSetChainSerializer

TWOPLACES = Decimal(10)**-2

class LegoSetList(APIView):
    """
    List all Lego sets
    """
    def get(self, request, format=None):
        legosets = LegoSet.objects.all()
        serializer = LegoSetSerializer(legosets, many=True)
        return Response(serializer.data)

class LegoSetDetail(APIView):
    """
    Retrieve, update or delete a legoset instance.
    """
    def get_object(self, pk):
        try:
            return LegoSet.objects.get(pk=pk)
        except LegoSet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        legoset = self.get_object(pk)
        serializer = LegoSetSerializer(legoset)
        return Response(serializer.data)

class LegoSetMonth(APIView):
    def get(self, request, format=None):
        grouping = []
        dates = LegoSet.objects.values_list('date_acquired', flat=True)
        months = set([(date.year, date.month) for date in dates if date != None])
        months = sorted(list(months))

        for (year, month) in months:
            legosets = LegoSet.objects.filter(date_acquired__year=year, date_acquired__month=month)
            # TODO generalise from here to the end
            count = legosets.count()
            aggregates = legosets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'year': year, 'month': month, 'legosets': legosets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            grouping.append(row)

        serializer = LegoSetMonthSerializer(grouping, many=True)
        return Response(serializer.data)

class LegoSetChain(APIView):
    def get(self, request, format=None):
        grouping = []

        chains = LegoSet.objects.all().values_list("chain", flat=True)
        chains = sorted(list(set(chains)))

        for chain in chains: 
            legosets = LegoSet.objects.filter(chain=chain)
            count = legosets.count()
            aggregates = legosets.aggregate(Sum('total_price'), Avg('total_price'))

            row = {'chain': chain, 'legosets': legosets, 'count': count}
            row['total_price'] = aggregates['total_price__sum']
            row['average_price'] = Decimal(aggregates['total_price__avg']).quantize(TWOPLACES)

            grouping.append(row)

        print grouping

        serializer = LegoSetChainSerializer(grouping, many=True)
        return Response(serializer.data)


