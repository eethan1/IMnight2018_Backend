from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "http://night2018.ntu.im/template.html"
        return path.format(username=request.user.username)
