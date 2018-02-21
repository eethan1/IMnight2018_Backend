from django.conf.urls import url
from sky.views import NewsListView

urlpatterns = [
    url(r'^news/$', NewsListView.as_view()),
]
