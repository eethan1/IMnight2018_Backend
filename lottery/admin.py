from django.contrib import admin
from lottery.models import Task, ProgressTask

from IMnight.utils import ModelWithLabelAdmin

admin.site.register(Task, ModelWithLabelAdmin)
admin.site.register(ProgressTask)
