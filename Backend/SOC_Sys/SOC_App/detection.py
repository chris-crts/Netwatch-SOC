from .models import NetworkEvent, SecurityIncident
from django.utils import timezone

def detect(event):
    ip = event.device.ip_address
    recent = NetworkEvent.objects.filter(device=event.device)

    failed_logins = recent.filter(action="login_failed").count()
    scans = recent.filter(action="port_scan").count()

    if failed_logins >= 5:
        SecurityIncident.objects.create(
            incident_type="BRUTE_FORCE",
            severity="HIGH",
            ip_address=ip,
            description="Multiple failed login attempts detected"
        )

    if scans >= 10:
        SecurityIncident.objects.create(
            incident_type="PORT_SCAN",
            severity="MEDIUM",
            ip_address=ip,
            description="Sequential port scanning detected"
        )