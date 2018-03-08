# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from human.models import Relationship
from human.chat.serializers import MessageSerializer


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

        messages = room.messages.order_by('timestamp')

        # query_range = self.request.query_params.get('query_range', None)
        # if query_range is not None:
        #     start, end = query_range.split('-')
        #

        return messages
