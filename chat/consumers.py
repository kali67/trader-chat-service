from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.conversation_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'chat_%s' % self.conversation_name

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_send(self.group_name, {
            'type': "send.message",
            "message": "User has joined the room!"
        })
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(self.group_name, {
            'type': "send.message",
            "message": "User has left the room"
        })

    async def receive(self, text_data):  # event is the text received from the client
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(self.group_name, {
            'type': "send.message",
            "message": message
        })

    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
