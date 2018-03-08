from rest_framework import serializers

from sky.models import Article, News, Course
from lottery.serializers import TaskSerializer


class CourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = ('id', 'name', 'teacher', 'label', 'img')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article

        fields = ('id', 'title', 'label', 'img')


class ArticleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(required=True)

    class Meta:
        model = Article

        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News

        fields = '__all__'
