from django.contrib import admin
from django import forms

from earth.models import HoldingVocher, Store, Vocher
from IMnight.utils import ModelWithLabelAdmin


class VocherModelForm(forms.ModelForm):
    class Meta:
        model = Vocher
        fields = '__all__'

    def fields_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            data = self.cleaned_data.get(field, '')
            if not data:
                msg = forms.ValidationError("This field is required.")
                self.add_error(field, msg)
            if data == 0:
                msg = forms.ValidationError(
                    "This field can't be zero when limit is on.")
                self.add_error(field, msg)

    def clean(self):
        super().clean()
        category = self.cleaned_data.get('category')

        if category != 1:
            self.fields_required(['limit'])
        else:
            self.cleaned_data['limit'] = 0

        return self.cleaned_data


class VocherAdmin(admin.ModelAdmin):
    form = VocherModelForm


admin.site.register(HoldingVocher, ModelWithLabelAdmin)
admin.site.register(Store)
admin.site.register(Vocher, VocherAdmin)
