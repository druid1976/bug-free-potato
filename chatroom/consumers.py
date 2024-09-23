import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Room
from accounts.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"