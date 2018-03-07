from django.conf.urls import url
from sky.views import NewsListView, ArticleListView, CourseListView, ArticleView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
    url(r'^list/articles/$', ArticleListView.as_view()),
    url(r'^article/$', ArticleView.as_view()),
    url(r'^courses/$', CourseListView.as_view()),
]
