import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MovieNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("movie_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("movie_notifications", self.channel_name)

    async def receive(self, text_data):
        pass  # No incoming messages needed

    async def movie_added(self, event):
        await self.send(text_data=json.dumps({
            'type': 'movie_added',
            'movie': event['movie']
        }))