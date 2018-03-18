from django.conf.urls import url
from earth.views import DailyVocherView, StoreVocherView, use_vocher, ListVocherView, ListStoreView

urlpatterns = [
    url(r'^vocher/$', StoreVocherView.as_view()),
    url(r'^list/vocher/$', ListVocherView.as_view()),
    url(r'^list/store/(?P<show>.+)/$', ListStoreView.as_view()),
    url(r'^vocher/(?P<storename>.+)/$', StoreVocherView.as_view()),
    url(r'^daily/$', DailyVocherView.as_view()),
    url(r'^use/vocher/$', use_vocher),
]
