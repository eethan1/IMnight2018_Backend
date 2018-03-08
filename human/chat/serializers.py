from rest_framework import serializers

from human.chat.models import Message
from human.serializers import RelationshipSerializer


class MessageSerializer(serializers.ModelSerializer):
    room = RelationshipSerializer(required=True)

    class Meta:
        model = Message
        fields = '__all__'
