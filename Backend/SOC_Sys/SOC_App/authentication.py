from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Device, DeviceToken


class DeviceTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("X-Device-Token")
        if not token:
            return None
        try:
            device_token = DeviceToken.objects.select_related("device").get(key=token, is_active=True)
        except DeviceToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive device token")
        if not device_token.device.is_active:
            raise AuthenticationFailed("Device is not active")
        return (device_token.device, device_token)


class IsAuthenticatedOrReadOnlyDevice(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return isinstance(request.user, Device)
