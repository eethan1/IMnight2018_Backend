from django.contrib import admin


class ModelWithLabelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return ['label', ]
