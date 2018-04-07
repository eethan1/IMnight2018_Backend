# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from human.chat.models import Message
from human.chat.serializers import MessageSerializer
from human.models import Relationship
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def read_message(request):
    """
    記得一定要設 contentType: "application/json" 才會用payload 而不是 formdata
    """
    if 'label' not in request.data:
        return Response({"message": "parameter \'label\' not in scoope"}, status=status.HTTP_400_BAD_REQUEST)
    if 'username' not in request.data:
        return Response({"message": "parameter \'username\' not in scoope"}, status=status.HTTP_400_BAD_REQUEST)

    chatroom = Relationship.objects.get(label=request.data['label'])
    read_handler = User.objects.get(username=request.data['username'])

    read_messages = Message.objects.filter(
        room=chatroom, handle=read_handler, readed=False)

    for msg in read_messages:
        msg.readed = True
        msg.save()
    return Response({"message": "Read Succeesslly"})


class ChatView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = MessageSerializer

    def get_queryset(self):

        if 'label' not in self.kwargs:
            # wrong url setting
            return []

        label = self.kwargs['label']
        try:
            room = Relationship.objects.get(label=label)
        except Relationship.DoesNotExist:
            print ("ws room does not exist label=%s", label)
            return []

        if room.client != self.request.user and room.performer != self.request.user:
            return []

        messages = room.messages.order_by('timestamp')

        # query_range = self.request.query_params.get('query_range', None)
        # if query_range is not None:
        #     start, end = query_range.split('-')
        #

        return messages
