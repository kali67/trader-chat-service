from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, scope):
        super().__init__(scope)
        self.conversation_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'chat_%s' % self.conversation_name

    async def connect(self):
        print("sfksanfslkfkasfsfhsakfslkfashf;salfhsfs;alfksaaf")
        await self.accept()
        #check users here
     #   print(json.loads(self.scope['user'])['username'])
        await self.channel_layer.group_send(self.group_name, {
            'type': "send.message",
            "message": {
                "message" : "User ",# + json.loads(self.scope['user'])['username'] + "  has joined the room",
                "username" : "none"
            }
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
            "message": {
                "message" : "User ",# + json.loads(self.scope['user'])['username'] + "  has left the room",
                "username" : "none"
            }
        })

    async def receive(self, text_data):  # event is the text received from the client
        text_data_json = json.loads(text_data)
        message = {
            "username": "",#json.loads(self.scope['user'])['username'],
            "message": text_data_json['message']
        }
        await self.channel_layer.group_send(self.group_name, {
            'type': "send.message",
            "message": message
        })

    async def send_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
