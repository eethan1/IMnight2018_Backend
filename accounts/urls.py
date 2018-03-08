from django.conf.urls import url

from accounts.views import check_login, dailyStatusCheck

urlpatterns = [
    url(r'^check/login/$', check_login),
    url(r'^check/daily/$', dailyStatusCheck),
]
