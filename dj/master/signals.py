from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from decimal import Decimal
from .models import Server

@receiver(post_save, sender=Server)
def notify_balance_update(sender, instance, created, **kwargs):
    # print(instance.balance)

    channel_layer = get_channel_layer()
    group_name = f'user_{instance.id}'

    payload = {
        'type': 'send_balance_data',
        'new_balance': str(instance.balance)
    }

    async_to_sync(channel_layer.group_send)(group_name, payload)