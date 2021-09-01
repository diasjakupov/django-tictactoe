from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import GameInfo
from .utils.gameManager import GameManager


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id=self.scope["url_route"]["kwargs"]["game_id"]
        self.game_name=f"game_{self.game_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.game_name,
            self.channel_name
        )
        self.manager=GameManager(self.scope['user'])
        print("Connect to game")
        isConnected=self.manager.connectToGame(self.game_id)
        print(isConnected)
        self.accept()

    def receive(self, text_data, bytes_data):
        return super().receive(text_data=text_data, bytes_data=bytes_data)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_name,
            self.channel_name
        )