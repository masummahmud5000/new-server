import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import RefreshToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

# database function class এর বাইরে
@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

class BalanceSlash(AsyncWebsocketConsumer):

    async def connect(self):
        # URL query থেকে token নেওয়া
        qs = parse_qs(self.scope["query_string"].decode())
        token = qs.get("token", [None])[0]

        if not token:
            await self.close()
            return

        try:
            access = RefreshToken(token)
            user_id = access["user_id"]
            self.scope["user"] = await get_user(user_id)
        except Exception as e:
            await self.close()
            return

        user = self.scope["user"]
        if not user:
            await self.close()
            return

        # group join
        self.group_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_init(user)

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def send_init(self, user):
        await self.send(text_data=json.dumps({
            'balance': str(user.balance)
        }))
    
    async def send_balance_data(self, event):
        await self.send(text_data=json.dumps({
            "balance": str(event["new_balance"])
        }))
