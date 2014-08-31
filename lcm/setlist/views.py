from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LegoSet
from .serializers import LegoSetSerializer

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

