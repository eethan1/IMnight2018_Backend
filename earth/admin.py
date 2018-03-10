from django.contrib import admin
from earth.models import HoldingVocher, Store, Vocher
from IMnight.utils import ModelWithLabelAdmin


admin.site.register(HoldingVocher, ModelWithLabelAdmin)
admin.site.register(Store)
admin.site.register(Vocher)
