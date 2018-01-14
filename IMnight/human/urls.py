from django.conf.urls import url
from human.views import SelfDetailsView, UserDetailsView, RelationshipDetailsView, DailyPerformerView

urlpatterns = [
    url(r'^user/$', UserDetailsView.as_view()),
    url(r'^user/self/$', SelfDetailsView.as_view()),
    url(r'^user/(?P<username>.+)/$', UserDetailsView.as_view()),
    url(r'^performer/list/$', RelationshipDetailsView.as_view()),
    url(r'^daily/$', DailyPerformerView.as_view()),
]
