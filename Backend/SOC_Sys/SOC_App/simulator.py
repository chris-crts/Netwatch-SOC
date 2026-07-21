import random
from .models import Device, NetworkEvent
from .detection import detect
from .broadcasting import broadcast_soc_event


def simulate_attack():
    devices = Device.objects.all()
    if not devices:
        return None

    device = random.choice(devices)
    actions = ["login_failed", "port_scan", "http_probe"]
    action = random.choice(actions)

    event = NetworkEvent.objects.create(
        device=device,
        action=action,
        service="ssh"
    )

    broadcast_soc_event({
        "type": "event",
        "ip_address": device.ip_address,
        "action": event.action,
        "service": event.service
    })

    detect(event)
    return event