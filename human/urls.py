from django.conf.urls import url
from human.views import SelfDetailsView, UserDetailsView, RelationshipDetailsView, DailyPerformerView, performer_profile
from human.chat.views import ChatView

urlpatterns = [
    url(r'^user/$', UserDetailsView.as_view()),
    url(r'^user/self/$', SelfDetailsView.as_view()),
    url(r'^user/(?P<username>.+)/$', UserDetailsView.as_view()),
    url(r'^performer/list/$', RelationshipDetailsView.as_view()),
    url(r'^daily/$', DailyPerformerView.as_view()),

    url(r'^chat/(?P<label>.+)/$', ChatView.as_view()),
    url(r'^modify/profile/', performer_profile)
]
