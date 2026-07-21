from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceViewSet,
    NetworkEventViewSet,
    SecurityIncidentViewSet,
    FirewallRuleViewSet,
    TrafficLogViewSet,
    incident_stats,
    simulate,
    lan_status,
    system_config,
)

router = DefaultRouter()
router.register('devices', DeviceViewSet)
router.register('events', NetworkEventViewSet)
router.register('incidents', SecurityIncidentViewSet)
router.register('firewall-rules', FirewallRuleViewSet)
router.register('traffic-logs', TrafficLogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/stats/', incident_stats),
    path('api/simulate/', simulate),
    path('api/lan-status/', lan_status),
    path('api/config/', system_config),
]