from rest_framework import serializers
from .models import Device, NetworkEvent, SecurityIncident, FirewallRule, TrafficLog


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class NetworkEventSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(source='device.ip_address', read_only=True)

    class Meta:
        model = NetworkEvent
        fields = ['id', 'device', 'ip_address', 'action', 'service', 'timestamp']


class SecurityIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIncident
        fields = '__all__'


class FirewallRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirewallRule
        fields = '__all__'


class TrafficLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficLog
        fields = '__all__'