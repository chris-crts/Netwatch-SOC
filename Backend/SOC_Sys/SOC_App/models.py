from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=50)
    name = models.CharField(max_length=100, default="unknown")
    is_active = models.BooleanField(default=True)

class NetworkEvent(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    service = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class SecurityIncident(models.Model):
    incident_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    ip_address = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
