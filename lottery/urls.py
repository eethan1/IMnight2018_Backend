from django.conf.urls import url
from lottery.views import ProgressTaskView, finish_task, TaskView


urlpatterns = [
    url(r'^progress_task/$', ProgressTaskView.as_view()),
    url(r'^progress_task/(?P<storename>.+)/$', ProgressTaskView.as_view()),
    url(r'^finish/$', finish_task),
    url(r'^tasks/$', TaskView.as_view()),
    url(r'^tasks/(?P<storename>.+)/$', TaskView.as_view()),
]
