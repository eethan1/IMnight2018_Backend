from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from accounts.serializers import (
    TokenSerializer, UserDetailsSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    PasswordChangeSerializer, JWTSerializer
)

from human.models import Relationship
from earth.models import HoldingVocher

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def check_login(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return Response({"auth_status": True})
    else:
        return Response({"auth_status": False})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def dailyStatusCheck(request):
    user = request.user
    is_drawn_daily_performer = Relationship.objects.check_daily(user)
    is_drawn_daily_vocher = HoldingVocher.objects.check_daily(user)
    return Response(
        {"performer_drawn": is_drawn_daily_performer,
         "vocher_drawn": is_drawn_daily_vocher}
    )
