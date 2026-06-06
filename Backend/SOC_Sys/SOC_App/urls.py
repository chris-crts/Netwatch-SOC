from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, NetworkEventViewSet, SecurityIncidentViewSet

router = DefaultRouter()
router.register('devices', DeviceViewSet)
router.register('events', NetworkEventViewSet)
router.register('incidents', SecurityIncidentViewSet)

urlpatterns = [
    path('', include(router.urls))
]