from django.conf.urls import url
from sky.views import NewsListView, ArticleListView, CourseListView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
    url(r'^articles/$', ArticleListView.as_view()),
    url(r'^courses/$', CourseListView.as_view()),
]
