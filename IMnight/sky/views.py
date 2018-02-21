from django.shortcuts import render

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

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
