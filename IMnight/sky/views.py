from django.shortcuts import render

from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from sky.models import Article, News, Course
from sky.serializers import NewsSerializer, ArticleSerializer, CourseSerializer, ArticleListSerializer

QUERY_MAX = 10


class CourseListView(ListAPIView):
    """
    取得課程
    default_para = {'index':'0', 'num':'5', 'label':None}
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer

    default_para = {'index': '0', 'num': '5', 'label': None}
    para_key = ('index', 'num', 'label')

    def get_queryset(self):
        q = {}
        for key in self.para_key:
            q[key] = self.request.query_params.get(key, self.default_para[key])
        queryset = Course.objects.all()
        if int(q['num']) > QUERY_MAX:
            q['num'] = QUERY_MAX
        if q['label'] is not None:
            queryset = queryset.filter(label=q['label'])
        queryset = queryset.order_by(
            '-created')[int(q['index']):int(q['index']) + int(q['num'])]
        return queryset


class ArticleListView(ListAPIView):
    """
    取得文章
    default_para = {'index':'0', 'num':'5', 'label':None}
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = ArticleListSerializer
    default_para = {'index': '0', 'num': '5', 'label': None}
    para_key = ('index', 'num', 'label')

    def get_queryset(self):
        q = {}
        for key in self.para_key:
            q[key] = self.request.query_params.get(key, self.default_para[key])
        queryset = Article.objects.all()
        if int(q['num']) > QUERY_MAX:
            q['num'] = QUERY_MAX
        if q['label'] is not None:
            queryset = queryset.filter(label=q['label'])
        queryset = queryset.order_by(
            '-created')[int(q['index']):int(q['index']) + int(q['num'])]
        return queryset


class ArticleView(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        label = self.request.query_params.get('label', None)
        queryset = Article.objects.none()
        if label is not None:
            queryset = Article.objects.filter(label=label)
        return queryset


class NewsListView(ListAPIView):
    """
    取得News
    default_para = {'index':'0', 'num':'5', 'label':None}
    """
    # permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer

    default_para = {'index': '0', 'num': '5', 'label': None}
    para_key = ('index', 'num', 'label')

    def get_queryset(self):
        q = {}
        for key in self.para_key:
            q[key] = self.request.query_params.get(key, self.default_para[key])
        queryset = News.objects.all()
        if int(q['num']) > QUERY_MAX:
            q['num'] = QUERY_MAX
        if q['label'] is not None:
            queryset = queryset.filter(label=q['label'])
        queryset = queryset.order_by(
            '-created')[int(q['index']):int(q['index']) + int(q['num'])]
        return queryset
