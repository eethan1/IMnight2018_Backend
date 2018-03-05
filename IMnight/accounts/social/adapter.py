from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "https://ck20jimmy.github.io/2018_IMNight_FrontEnd/view/template.html"
        return path.format(username=request.user.username)
