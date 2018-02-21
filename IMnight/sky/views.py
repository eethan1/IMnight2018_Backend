from django.shortcuts import render

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from sky.models import Article, News
from sky.serializers import NewsSerializer, ArticleSerializer


class NewsListView(ListAPIView):
    """
    取得用戶自己以抽過的performer
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all().order_by('-created')[:5]
        return queryset


class CreateNewsView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer

    # def create(request, *args, **kwargs):
    #     if request.user.groups.filter(name='Admin').exists():
    #         super(CreateNewsView, self).create(request, *args, **kwargs)
    #     else:
    #         raise
