import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMnight.im_settings")
django.setup()


from allauth.socialaccount.models import SocialAccount

accounts = SocialAccount.objects.all()
preferred_avatar_size_pixels = 500

for account in accounts:
    if account.user.profile.img == "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/10712978_745859095491727_8519447814807561759_n.jpg?oh=51a1b3c040bebb38f221053aeb2c42db&oe=5B16C07D":
        print(account.user)
        picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(
            account.uid, preferred_avatar_size_pixels)
        account.user.username = account.extra_data['name']
        account.user.profile.img = picture_url
        account.user.save()
