from django.conf.urls import url
from sky.views import NewsListView, CreateNewsView, ArticleListView, CourseListView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
    url(r'^create/news', CreateNewsView.as_view()),
    url(r'^articles', ArticleListView.as_view()),
    url(r'^courses', CourseListView.as_view()),
]
