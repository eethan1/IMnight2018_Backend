import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from human.models import Profile, Relationship
from human.serializers import RelationshipSerializer, UserDetailsSerializer
from rest_framework import status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

log = logging.getLogger('syslogger')

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
            # sort by unread_msg_count while querying
            queryset = Relationship.objects.filter(
                Q(client=user) | Q(performer=user)).annotate(
                unread_msg_count=Count('messages')).order_by('-unread_msg_count')

        except Exception as error:
            log.warning("query %s Relationship發生錯誤: %s" %
                        (user.username, error))
        else:
            for relationship in queryset:
                if relationship.performer == user:
                    tmp = relationship.performer
                    relationship.performer = relationship.client
                    relationship.client = tmp
                    # !!! DO NOT SAVE HERE
                    # this is the quick fix
                    # but not well written
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['job', 'job_description', 'bio', 'img']


@login_required
def performer_profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect('https://ntu.im/night/2018/home.html')

    form = ProfileForm(instance=request.user.profile)
    return render(request, 'performer_profile.html', {'form': form})
