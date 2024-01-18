from django.forms import ModelForm
from .models import Status


class StatusCreateForm(ModelForm):
    class Meta:
        model = Status
        fields = (
            'name',
        )


class StatusUpdateForm(ModelForm):
    class Meta:
        model = Status
        fields = (
            'name',
        )

    def clean_name(self):
        return self.cleaned_data.get('name')
