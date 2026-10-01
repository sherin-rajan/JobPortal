from django.shortcuts import render
from api.serializers import SectorSerializer,JobSerializer
from jobs.models import Sectors,Jobs
from rest_framework.generics import ListAPIView,ListCreateAPIView

# Create your views here.
class SectorSerializer(ListAPIView):
    queryset=Sectors.objects.all()
    serializer_class=SectorSerializer

class JobSerializer(ListCreateAPIView):
    queryset=Jobs.objects.all()
    serializer_class=JobSerializer

