from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter, DefaultSocialAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = "https://ntu.im/night/2018/view/template.html"
        # return path.format(username=request.user.username)
        return path

    def get_logout_redirect_url(self, request):
        path = "https://ntu.im/night/2018/view/homepage.html"
        # return path.format(username=request.user.username)
        return path


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        path = "https://ntu.im/night/2018/view/template.html"
        # return path.format(username=request.user.username)
        return path
