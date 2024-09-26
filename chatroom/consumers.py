import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, **kwargs):
        text_data_json = json.loads(kwargs.get('text_data'))
        message = text_data_json['message']
        note = text_data_json['note']
        user = self.scope['user']

        if note == 1:
            await self.save_message(user, self.room_name, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def save_message(self, user, room_name, message):
        room = Room.objects.get(name=room_name)
        return Message.objects.create(user=user, room=room, content=message)
