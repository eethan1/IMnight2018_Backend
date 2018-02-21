from django.conf.urls import url
from sky.views import NewsListView, CreateNewsView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
    url(r'^create/news', CreateNewsView.as_view()),
]
