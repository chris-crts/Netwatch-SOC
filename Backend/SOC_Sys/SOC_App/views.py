from django.shortcuts import render
from .detection import detect
from .simulator import simulate_attack

from rest_framework import viewsets
from .models import Device, NetworkEvent, SecurityIncident
from .serializers import DeviceSerializer, NetworkEventSerializer, SecurityIncidentSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SecurityIncident

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class NetworkEventViewSet(viewsets.ModelViewSet):
    queryset = NetworkEvent.objects.all()
    serializer_class = NetworkEventSerializer

class SecurityIncidentViewSet(viewsets.ModelViewSet):
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer

def perform_create(self, serializer):
    event = serializer.save()
    detect(event)
    
@api_view(['GET'])
def incident_stats(request):
    data = {
        "BRUTE_FORCE": SecurityIncident.objects.filter(incident_type="BRUTE_FORCE").count(),
        "PORT_SCAN": SecurityIncident.objects.filter(incident_type="PORT_SCAN").count(),
    }
    return Response(data)
  
@api_view(['POST'])
def simulate(request):
    simulate_attack()
    return Response({"status": "ok"})