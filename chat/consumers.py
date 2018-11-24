from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from datetime import datetime

from .serializers import MessageSerializer
from .models import *
import json


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.group_name = 'chat_%s' % self.conversation_id
        self.user = json.loads(self.scope['user'])

    async def connect(self):
        # check users here
        user_incoming = dict(json.loads(self.scope['user']))
        await self.accept()
        if 'username' in user_incoming:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            await self.send(text_data=json.dumps({
                "message": {
                    "username": "",
                    "message": "Unauthorized - please log in or supply valid access token"
                }
            }))
            await self.send(text_data={}, close=True)

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        if 'username' in self.scope['user']:  # if was an actual user - emit that they left to the group
            await self.channel_layer.group_send(self.group_name, {
                'type': "send.message",
                "message": {
                    "message": "User " + json.loads(self.scope['user'])['username'] + "  has left the room",
                    "username": "none"
                }
            })

    async def receive(self, text_data):  # event is the text received from the client
        text_data_json = json.loads(text_data)
        message = Message(conversation_id=int(self.conversation_id),
                          user_id=int(self.user['user_id']),
                          content=str(text_data_json['message']),
                          sent_timestamp= datetime.now())
        message.save()
        #await database_sync_to_async(message.save())()  # db call async - returns wrapped function as async function

        message_serializer = MessageSerializer(instance=message)
        await self.channel_layer.group_send(self.group_name, {
                'type': "send.message",
                "message": message_serializer.data
            })

    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
