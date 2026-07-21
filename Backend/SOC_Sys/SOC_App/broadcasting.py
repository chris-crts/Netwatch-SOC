from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

SOC_GROUP = "soc_group"


def broadcast_soc_event(data):
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        async_to_sync(channel_layer.group_send)(
            SOC_GROUP,
            {"type": "soc_message", "data": data},
        )
