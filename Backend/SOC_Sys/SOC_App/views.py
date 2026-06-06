from django.shortcuts import render

from rest_framework import viewsets
from .models import Device, NetworkEvent, SecurityIncident
from .serializers import DeviceSerializer, NetworkEventSerializer, SecurityIncidentSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class NetworkEventViewSet(viewsets.ModelViewSet):
    queryset = NetworkEvent.objects.all()
    serializer_class = NetworkEventSerializer

class SecurityIncidentViewSet(viewsets.ModelViewSet):
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer
