from importlib import import_module
from django.conf.urls import url

from .views import FacebookLogin, facebookButton

from allauth.socialaccount import providers


urlpatterns = [
    # url(r'^facebook/token$', FacebookLogin.as_view(), name='fb_login'),
    # url(r'^facebook/button$', facebookButton),
]

# for provider in providers.registry.get_list():
#     try:
#         prov_mod = import_module(provider.get_package() + '.urls')
#     except ImportError:
#         continue
#     prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
#     if prov_urlpatterns:
#         urlpatterns += prov_urlpatterns
