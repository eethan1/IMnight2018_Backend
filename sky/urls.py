from django.conf.urls import url
from sky.views import NewsListView, ArticleListView, CourseListView, ArticleView, CourseView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
    url(r'^list/articles/$', ArticleListView.as_view()),
    url(r'^article/(?P<label>.+)/$', ArticleView.as_view()),
    url(r'^list/courses/$', CourseListView.as_view()),
    url(r'^course/(?P<label>.+)/$', CourseView.as_view()),
]
