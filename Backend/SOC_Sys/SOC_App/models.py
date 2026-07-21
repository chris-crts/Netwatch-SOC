import secrets
from django.db import models


class Device(models.Model):
    ip_address = models.CharField(max_length=50)
    name = models.CharField(max_length=100, default="unknown")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class DeviceToken(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="token")
    key = models.CharField(max_length=64, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token for {self.device.name}"


class NetworkEvent(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    service = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]


class SecurityIncident(models.Model):
    incident_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    ip_address = models.CharField(max_length=50)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]


class FirewallRule(models.Model):
    ACTION_CHOICES = [("ALLOW", "ALLOW"), ("BLOCK", "BLOCK")]

    ip_address = models.CharField(max_length=50, db_index=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default="BLOCK")
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("ip_address", "action")


class TrafficLog(models.Model):
    ip_address = models.CharField(max_length=50, db_index=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(default=0)
    blocked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]


class SystemConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)

    @staticmethod
    def get(key, default=None):
        obj = SystemConfig.objects.filter(key=key).first()
        return obj.value if obj else default

    @staticmethod
    def set(key, value):
        obj, _ = SystemConfig.objects.update_or_create(key=key, defaults={"value": value})
        return obj

    def __str__(self):
        return f"{self.key} = {self.value}"