from django import forms
from django.forms import ModelForm

from .models import Task
from task_manager.labels.models import Label


class TaskCreateForm(ModelForm):

    class Meta:
        label = forms.ModelMultipleChoiceField(
            queryset=Label.objects.all(),
            widget=forms.Select(attrs={
                'class': 'form-select',
                'multiply': 'multiply'
            }),
            required=False,
        )
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels'
        )


class TaskUpdateForm(ModelForm):
    class Meta:
        label = forms.ModelMultipleChoiceField(
            queryset=Label.objects.all(),
            widget=forms.Select(attrs={
                'class': 'form-select',
                'multiply': 'multiply'
            }),
            required=False,
        )
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'executor',
            'labels',
        )

    def clean_name(self):
        return self.cleaned_data.get('name')
