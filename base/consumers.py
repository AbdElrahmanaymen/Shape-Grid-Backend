import datetime
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Shape


class ShapesConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling shapes-related events.

    This consumer handles the connection, disconnection, and message receiving
    events for the shapes WebSocket channel. It also provides methods for adding,
    updating, and deleting shapes.

    Attributes:
        channel_name (str): The name of the channel associated with the consumer.

    Methods:
        connect: Called when the WebSocket is handshaking as part of the connection process.
        get_data_from_database: Retrieves data from the database asynchronously.
        receive: Called when a WebSocket frame is received from the client.
        shapes_add: Called when a new shape is added.
        shapes_update: Called when a shape is updated.
        shapes_delete: Called when a shape is deleted.
        disconnect: Called when the WebSocket closes for any reason.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        """
        await self.channel_layer.group_add("shapes", self.channel_name)
        await self.accept()

        # Retrieve data from the database
        data = await self.get_data_from_database()
        await self.send(text_data=json.dumps({"type": "shapes.initial", "data": data}))

    @database_sync_to_async
    def get_data_from_database(self):
        """
        Retrieves data from the database asynchronously.
        """
        items = Shape.objects.all().values()
        items_data = list(items)
        for item in items_data:
            for key, value in item.items():
                if isinstance(value, datetime.datetime):
                    item[key] = value.isoformat()
        return items_data

    async def receive(self, text_data):
        """
        Called when a WebSocket frame is received from the client.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send the received message back to the client
        await self.send(text_data=json.dumps({'message': message}))

    async def shapes_add(self, event):
        """
        Called when a new shape is added.
        """
        data = event["data"]
        await self.send(text_data=json.dumps({"type": "shapes.add", "data": data}))

    async def shapes_update(self, event):
        """
        Called when a shape is updated.
        """
        data = event["data"]
        await self.send(text_data=json.dumps({"type": "shapes.update", "data": data}))

    async def shapes_delete(self, event):
        """
        Called when a shape is deleted.
        """
        data = event["data"]
        await self.send(text_data=json.dumps({"type": "shapes.delete", "data": data}))

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard("shapes", self.channel_name)
