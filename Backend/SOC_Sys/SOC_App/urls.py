from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, NetworkEventViewSet, SecurityIncidentViewSet
from .views import incident_stats, simulate

router = DefaultRouter()
router.register('devices', DeviceViewSet)
router.register('events', NetworkEventViewSet)
router.register('incidents', SecurityIncidentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/stats/', incident_stats),
    path('api/simulate/', simulate),
]

