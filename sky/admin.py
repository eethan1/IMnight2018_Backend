from django.contrib import admin
from sky.models import Article, News, Course

from IMnight.utils import ModelWithLabelAdmin

admin.site.register(Article, ModelWithLabelAdmin)
admin.site.register(News, ModelWithLabelAdmin)
admin.site.register(Course, ModelWithLabelAdmin)
