from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import GameInfo
from .utils.gameManager import GameManager
import json


class GameConsumer(WebsocketConsumer):
    def connect(self):
        print("connect")
        self.game_id=self.scope["url_route"]["kwargs"]["game_id"]
        self.game_name=f"game_{self.game_id}"
        print("connect 1.5")

        async_to_sync(self.channel_layer.group_add)(
            self.game_name,
            self.channel_name
        )

        print("connect 2")
        self.manager=GameManager(self.scope['user'])
        self.manager.connectToGame(self.game_id)
        self.accept()
        self.first_connect(self.manager.sign)

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            newData, isEnded=self.manager.makeMove(message)
            chat_message=json.dumps({"movements": newData, "game_status": isEnded})

            if isEnded!=-1 and isEnded!=0:
                winUser=json.loads(newData)[-1]['userId']
                chat_message=json.dumps({"movements": newData, "game_status": isEnded, "winUser": winUser})
            
            print(chat_message)
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

    def first_connect(self, sign):
        self.send(text_data=json.dumps({
            'sign': sign
        }))