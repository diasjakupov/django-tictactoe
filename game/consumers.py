from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import GameInfo
from .utils.gameManager import GameManager
import json


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id=self.scope["url_route"]["kwargs"]["game_id"]
        self.game_name=f"game_{self.game_id}"
        self.manager=GameManager(self.scope['user'])
        self.manager.connectToGame(self.game_id)
        async_to_sync(self.channel_layer.group_add)(
            self.game_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
            message = text_data_json['message']
            x, y=message.split(',')
            newData, isEnded=self.manager.makeMove(x, y)

            chat_message=json.dumps({"movements": newData, "isEnded": isEnded})

            if isEnded!=-1 and isEnded!=0:
                winUser=json.loads(newData)[-1]['userId']
                chat_message=json.dumps({"movements": newData, "isEnded": isEnded, "winUser": winUser})
            
        
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.game_name,
                {
                    'type': 'chat_message',
                    'message': chat_message
                }
            
            )
        except Exception as e:
            print(e)

    def disconnect(self, code):
        print(code)
        async_to_sync(self.channel_layer.group_discard)(
            self.game_name,
            self.channel_name
        )

        # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))