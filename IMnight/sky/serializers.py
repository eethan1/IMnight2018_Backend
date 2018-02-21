from rest_framework import serializers

from sky.models import Article, News


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article

        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News

        fields = ('title', 'url')
