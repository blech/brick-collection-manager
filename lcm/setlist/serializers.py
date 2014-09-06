from rest_framework import serializers

from .models import LegoSet

class LegoSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegoSet

class LegoSetMonthSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField()
    average_price = serializers.DecimalField()

class LegoSetChainSerializer(serializers.Serializer):
    chain = serializers.CharField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField()
    average_price = serializers.DecimalField()

