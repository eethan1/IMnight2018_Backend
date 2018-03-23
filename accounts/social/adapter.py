from django.dispatch import receiver

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.signals import user_logged_in, user_signed_up
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = "https://ntu.im/night/2018/home.html"
        # return path.format(username=request.user.username)
        return path

    def get_logout_redirect_url(self, request):
        path = "https://ntu.im/night/2018/home.html"
        # return path.format(username=request.user.username)
        return path


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        path = "https://ntu.im/night/2018/home.html"
        # return path.format(username=request.user.username)
        return path


@receiver(user_signed_up)
def social_signup(sociallogin, user, **kwargs):
    preferred_avatar_size_pixels = 500
    if sociallogin.account.provider == 'facebook':
        picture_url = "https://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
            sociallogin.account.uid, preferred_avatar_size_pixels)
        user.username = sociallogin.account.extra_data['name']
        user.profile.img = picture_url
        user.save()


@receiver(user_logged_in)
def social_login(sociallogin, user, **kwargs):
    preferred_avatar_size_pixels = 500
    if sociallogin.account.provider == 'facebook':
        picture_url = "https://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
            sociallogin.account.uid, preferred_avatar_size_pixels)
        user.profile.img = picture_url
        user.save()
