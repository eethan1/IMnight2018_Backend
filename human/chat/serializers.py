from django.contrib.auth.models import User

from rest_framework import serializers

from human.chat.models import Message
from human.serializers import RelationshipSerializer, UserDetailsSerializer

class HandlerSerialier(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class MessageSerializer(serializers.ModelSerializer):
    #room = RelationshipSerializer(required=True)
    handle = HandlerSerialier(required=True)

    class Meta:
        model = Message
        fields = ("message", "handle", "timestamp", "readed")
