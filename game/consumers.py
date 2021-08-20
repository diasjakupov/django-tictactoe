from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        return super().connect()

    def receive(self, text_data, bytes_data):
        return super().receive(text_data=text_data, bytes_data=bytes_data)

    def disconnect(self, code):
        return super().disconnect(code)