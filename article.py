import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMnight.im_settings")
django.setup()


from sky.models import Article


articles = Article.objects.all()

for article in articles:
    print(article.content)
    article.content = article.content.replace('<br />', '<br /><br />')
    article.save()
