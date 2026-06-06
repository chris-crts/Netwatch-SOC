import random
from .models import Device, NetworkEvent

def simulate_attack():
    devices = Device.objects.all()
    if not devices:
        return

    device = random.choice(devices)

    actions = ["login_failed", "port_scan", "http_probe"]

    NetworkEvent.objects.create(
        device=device,
        action=random.choice(actions),
        service="ssh"
    )