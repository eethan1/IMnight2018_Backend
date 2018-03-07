from rest_framework import serializers

from sky.models import Article, News, Course
from lottery.serializers import TaskSerializer


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    task = TaskSerializer(required=True)

    class Meta:
        model = Article

        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News

        fields = '__all__'
