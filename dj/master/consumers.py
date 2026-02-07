import json
from channels.generic.websocket import WebsocketConsumer

class BalanceSlash(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'message': 'Connection Successfull'}))

    def receive(self, text_data):
        pass

    def disconnect(self, close_code):
        pass