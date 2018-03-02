from django.db import models
from django.utils import timezone
from django.utils.text import slugify

ARTICLE_CATEGORY_CHOICE = (
    (1, "故事"),
    (2, "課程"),
    (3, "學習資源")
)

class Course(models.Model):

    name = models.TextField(blank=False, default="課程名稱")
    teacher = models.TextField(blank=False, default="教師名稱")
    more = models.TextField(blank=False, default="教師名稱")
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    content = models.TextField(blank=True, default="內文")
    created = models.DateTimeField(default=timezone.now)    
    label = models.SlugField(unique=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        verbose_name = "Course"

    def __str__(self):
        return '%s teacher:%s label:%s' % (self.name, self.teacher, self.label)

    def save(self, *args, **kwargs):
        hashkey = self.name + str(self.created)
        course_label =  hash(hashkey) % (10 ** 20)
        course_label = slugify(course_label)
        try:
            self.label = course_label
        except Exception:
            course_label = hash(hashkey**2) % (10**20) 
            course_label = slugify(course_label)
            self.label = course_label

        super(Course, self).save(*args, **kwargs)


class Article(models.Model):
    title = models.TextField(blank=False, default="文章")
    category = models.SmallIntegerField(
        default=1, choices=ARTICLE_CATEGORY_CHOICE)
    content = models.TextField(blank=True, default="文章")
    detail = models.TextField(blank=True, default='文章')
    img = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    created = models.DateTimeField(default=timezone.now)
    label = models.SlugField(unique=True, blank=True)

    objects = models.Manager()
    class Meta:
        verbose_name = "Article"
    
    def __str__(self):
        return '%s %s label:%s' % (self.title, ARTICLE_CATEGORY_CHOICE[self.category-1][1], self.label)

    def save(self, *args, **kwargs):
        hashkey = self.title + str(self.created)
        article_label =  hash(hashkey) % (10 ** 20)
        article_label = slugify(article_label)
        try:
            self.label = article_label
        except Exception:
            article_label = hash(hashkey**2) % (10**20) 
            article_label = slugify(article_label)
            self.label = article_label

        super(Article, self).save(*args, **kwargs)



class News(models.Model):
    title = models.TextField(blank=False, default="最新消息")
    url = models.URLField(
        blank=False, default="https://i.imgur.com/67A5cyq.jpg")
    created = models.DateTimeField(default=timezone.now)
    label = models.SlugField(unique=True, blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "News"

    def save(self, *args, **kwargs):
        hashkey = self.title + str(self.created)
        news_label =  hash(hashkey) % (10 ** 20)
        news_label = slugify(news_label)
        try:
            self.label = news_label
        except Exception:
            news_label = hash(hashkey**2) % (10**20) 
            news_label = slugify(news_label)
            self.label = news_label

        super(News, self).save(*args, **kwargs)
