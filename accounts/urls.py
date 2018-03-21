from django.conf.urls import url

from accounts.views import check_login, dailyStatusCheck, finishReadTutorial

urlpatterns = [
    url(r'^check/login/$', check_login),
    url(r'^check/daily/$', dailyStatusCheck),
    url(r'^read/tutorial/$', finishReadTutorial)
]
