from django.contrib.auth.models import User

from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from human.models import Relationship
from human.chat.models import Message


import re
import json
import logging

testlog = logging.getLogger('testdevelop')


class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        """
        called when a websocket is create
        establish a websocket connection and add the user into a chatroom group
        """

        label = self.scope["url_route"]["kwargs"]["label"]
        self.user = self.scope["user"]

        try:
            room = Relationship.objects.get(label=label)
        except Relationship.DoesNotExist:
            testlog.error('No relationship have this label=%s', label)
            self.close()
            return
        except Exception as error:
            self.close()
            return

        if not (room.client == self.user or room.performer == self.user):
            testlog.warning(
                '%s try to connect to the relationship that not belog to him', self.user)
            self.close()
            return

        self.scope["room"] = room
        # Accept the incoming connection
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            "chat" + str(label), self.channel_name)

    def receive_json(self, content):

        self.user = self.scope["user"]
        room = self.scope["room"]
        label = self.scope["url_route"]["kwargs"]["label"]

        """
        called when message is recieved websocket
        """

        if content:
            if content["message"]:
                msg = content["message"]
                m = Message.objects.create(
                    room=room, handle=self.user, message=msg)

                async_to_sync(self.channel_layer.group_send)(
                    "chat" + str(label),
                    {
                        "type": "chat.message",
                        "text": json.dumps(m.as_dict()),
                    },
                )

        else:
            testlog.warning(
                "message data send by ws is NULL, full message: \n%s", message)

    def chat_message(self, event):
        self.send_json(event["text"])

    def disconnect(self, close_code):
        """
        called when websocket is closed
        """

        async_to_sync(self.channel_layer.group_discard)(
            "chat", self.channel_name)
