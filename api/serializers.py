from rest_framework import serializers
from jobs.models import Sectors,Jobs

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sectors
        fields=["id","name"]

class JobSerializer(serializers.ModelSerializer):
    sector=SectorSerializer(read_only=True)
    class Meta:
        model=Jobs
        fields="__all__"