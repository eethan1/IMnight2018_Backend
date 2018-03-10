from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
import coreapi

from human.models import Relationship
from human.serializers import UserDetailsSerializer, RelationshipSerializer

import logging
testlog = logging.getLogger('testdevelop')

UserModel = get_user_model()


class SelfDetailsView(RetrieveUpdateAPIView):
    """
    取得用戶自己的個人資料（Include Profile）
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return UserModel.objects.none()


class UserDetailsView(ListAPIView):
    """
    用username，取得特定用戶的資料（Include Profile）
    假如username留空，則會回傳所有用戶的資料（Include Profile）
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            queryset = queryset.filter(username=username)
        return queryset


class RelationshipDetailsView(ListAPIView):
    """
    取得用戶自己以抽過的performer
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RelationshipSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user

        try:
            queryset = Relationship.objects.get_performers(user)
        except ValidationError as error:
            testlog.error(error)
        except Exception as error:
            testlog.warning(error)
        else:
            return queryset


class DailyPerformerView(ListAPIView):
    """
    取得當日的daily performer
    當所有perfromer都被抽完之後會return []
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = RelationshipSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user

        queryset = Relationship.objects.get_daily(user)
        return queryset
