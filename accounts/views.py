import logging

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from earth.models import HoldingVocher
from human.models import Relationship
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

log = logging.getLogger('syslogger')

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def check_login(request):
    """
    檢查用戶是否已登入
    在任何的情況下都可以呼叫這個API，以Boolean值回傳用戶是否登入
    * auth_status => 使否已登入
    """
    if request.user.is_authenticated:
        return Response({
            "auth_status": True,
        })
    else:
        return Response({
            "auth_status": False,
        })


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def dailyStatusCheck(request):
    """
    檢查用後有沒有抽過當日優惠卷、表演者
    * performer_drawn => 是否抽過當日表演者
    * all_performers_drawn => 是否抽完全部的表演者
    * vocher_drawn => 是否抽過當日優惠券
    * is_read_tutorial => 有沒有看過教學動畫
    """
    user = request.user
    (is_performer_drawn, is_all_drawn) = Relationship.objects.check_daily(user)
    is_drawn_daily_vocher = HoldingVocher.objects.check_daily(user)
    is_read_tutorial = request.user.profile.isReadTutorial
    return Response({
        "performer_drawn": is_performer_drawn,
        "all_performers_drawn": is_all_drawn,
        "vocher_drawn": is_drawn_daily_vocher,
        "is_read_tutorial": is_read_tutorial
    })


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((SessionAuthentication, BasicAuthentication))
def finishReadTutorial(request):
    user = request.user
    if user:
        user.profile.isReadTutorial = True
        user.profile.save()
        return Response({
            "message": "Success",
        })
    else:
        return Response({
            "message": "Failed",
        })
