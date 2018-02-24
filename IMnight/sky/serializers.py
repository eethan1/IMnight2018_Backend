from rest_framework import serializers

from sky.models import Article, News, Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course

        # fields = '__all__'
        exclude = ('label',)

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article

        # fields = '__all__'
        exclude = ('label',)

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News

        # fields = '__all__'
        exclude = ('label',)
