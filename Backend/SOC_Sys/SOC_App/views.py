from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .models import Device, NetworkEvent, SecurityIncident, FirewallRule, TrafficLog, SystemConfig
from .serializers import (
    DeviceSerializer,
    NetworkEventSerializer,
    SecurityIncidentSerializer,
    FirewallRuleSerializer,
    TrafficLogSerializer,
)
from .detection import detect
from .simulator import simulate_attack
from .authentication import DeviceTokenAuthentication, IsAuthenticatedOrReadOnlyDevice


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class NetworkEventViewSet(viewsets.ModelViewSet):
    queryset = NetworkEvent.objects.all()
    serializer_class = NetworkEventSerializer
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnlyDevice]

    def perform_create(self, serializer):
        event = serializer.save()
        detect(event)


class SecurityIncidentViewSet(viewsets.ModelViewSet):
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer


class FirewallRuleViewSet(viewsets.ModelViewSet):
    queryset = FirewallRule.objects.all()
    serializer_class = FirewallRuleSerializer
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnlyDevice]


class TrafficLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TrafficLog.objects.all()[:200]
    serializer_class = TrafficLogSerializer


@api_view(['GET'])
def incident_stats(request):
    data = {
        "BRUTE_FORCE": SecurityIncident.objects.filter(incident_type="BRUTE_FORCE").count(),
        "PORT_SCAN": SecurityIncident.objects.filter(incident_type="PORT_SCAN").count(),
    }
    return Response(data)


@api_view(['GET'])
def lan_status(request):
    data = {
        "active_devices": Device.objects.filter(is_active=True).count(),
        "total_devices": Device.objects.count(),
        "total_events": NetworkEvent.objects.count(),
        "total_incidents": SecurityIncident.objects.count(),
        "blocked_ips": FirewallRule.objects.filter(action="BLOCK").count(),
    }
    return Response(data)


@api_view(['GET', 'POST'])
def system_config(request):
    if request.method == 'GET':
        configs = {c.key: c.value for c in SystemConfig.objects.all()}
        return Response(configs)

    key = request.data.get("key")
    value = request.data.get("value")
    if not key:
        return Response({"error": "key is required"}, status=400)

    SystemConfig.set(key, value)
    return Response({"key": key, "value": value})


@api_view(['POST'])
@authentication_classes([DeviceTokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnlyDevice])
def simulate(request):
    event = simulate_attack()
    if event is None:
        return Response({"status": "no_devices"})
    return Response({"status": "ok"})