from django.conf.urls import url
from lottery.views import ProgressTaskView, finish_task, get_tasks


urlpatterns = [
    url(r'^progress_task/$', ProgressTaskView.as_view()),
    url(r'^progress_task/(?P<storename>.+)/$', ProgressTaskView.as_view()),
    url(r'^finish/$', finish_task),
    url(r'^tasks/$', get_tasks),
]
