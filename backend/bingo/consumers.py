# bingo/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class GameConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "game_group",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "game_group",
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        musical = text_data_json['musical']
        self.send(text_data=json.dumps({
            'musical': musical
        }))

    def musical_selected(self, event):
        musical = event['musical']
        self.send(text_data=json.dumps({
            'musical': musical
        }))
