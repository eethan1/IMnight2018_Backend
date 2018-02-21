from django.db import models
from django.utils import timezone


ARTICLE_CATEGORY_CHOICE = (
    (1, "故事"),
    (2, "課程"),
    (3, "學習資源")
)


class Article(models.Model):
    title = models.TextField(blank=False, default="文章")
    category = models.SmallIntegerField(
        default=1, choices=ARTICLE_CATEGORY_CHOICE)
    content = models.TextField(blank=True, default="文章")
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")


class News(models.Model):
    title = models.TextField(blank=False, default="最新消息")
    url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "News"
