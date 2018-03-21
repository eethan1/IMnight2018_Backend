# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status


from earth.models import HoldingVocher, Store, Vocher
from earth.serializers import HoldingVocherSerializer, VocherSerializer, UseVocherSerializer, StoreSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def use_vocher(request):
    """
    記得一定要設 contentType: "application/json" 才會用payload 而不是 formdata
    """
    if ('label' in request.data):
        if HoldingVocher.objects.used_vocher(request.user, request.data['label']):
            return Response({"message": "Used Succeesslly"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Error occured when vocher used"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response({"message": "parameter \'label\' not in scoope"}, status=status.HTTP_400_BAD_REQUEST)


class DailyVocherView(ListAPIView):
    """
    取得當日的daily vocher
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = HoldingVocherSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = HoldingVocher.objects.get_daily(user)
        return queryset


class StoreVocherView(ListAPIView):
    """
    取得用戶的Vocher
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = HoldingVocherSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `storename` query parameter in the URL.
        """
        user = self.request.user
        if 'storename' in self.kwargs:
            storename = self.kwargs['storename']
            queryset = HoldingVocher.objects.get_vochers(user, storename)
        else:
            queryset = HoldingVocher.objects.get_vochers(user)
        return queryset


class ListVocherView(ListAPIView):
    """
    取得所有的vocher
    """
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = VocherSerializer

    def get_queryset(self):
        queryset = Vocher.objects.all()
        return queryset


class ListStoreView(ListAPIView):
    """
    取得所有的store
    """
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all()
        show = self.request.query_params.get('show', None)
        if show is not None:
            queryset = queryset.filter(show=show)
        return queryset
