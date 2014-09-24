from rest_framework import serializers

from .models import OwnedSet

class OwnedSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnedSet

class OwnedSetChainSerializer(serializers.Serializer):
    chain = serializers.CharField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField()
    average_price = serializers.DecimalField()

class OwnedSetMonthSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField()
    average_price = serializers.DecimalField()

class OwnedSetThemeSerializer(serializers.Serializer):
    theme = serializers.CharField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField()
    average_price = serializers.DecimalField()

