import json
from os import stat
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import manager
from game.utils.gameManager import GameManager

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.manager=GameManager(self.scope['user'])
        self.manager.createGameInstance()
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        newData, isEnded=self.manager.makeMove(message)

        chat_message=json.dumps({"movements": newData, "isEnded": isEnded})

        if isEnded!=-1 and isEnded!=0:
            winUser=json.loads(newData)[-1]['userId']
            chat_message=json.dumps({"movements": newData, "isEnded": isEnded, "winUser": winUser})
            
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat_message
            }
        )
        


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))