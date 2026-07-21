from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .models import FirewallRule, TrafficLog


class LANFirewallMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = self.get_client_ip(request)
        blocked = FirewallRule.objects.filter(ip_address=ip, action="BLOCK").exists()

        TrafficLog.objects.create(
            ip_address=ip,
            path=request.path,
            method=request.method,
            blocked=blocked,
        )

        if blocked:
            return JsonResponse({"error": "Access blocked by firewall policy"}, status=403)

    def get_client_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
