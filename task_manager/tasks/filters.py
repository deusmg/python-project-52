from django_filters import FilterSet, BooleanFilter, ModelChoiceFilter
from django.forms import CheckboxInput
from django.utils.translation import gettext as _
from .models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    only_my_tasks = BooleanFilter(
        label=_('Only my tasks'),
        widget=CheckboxInput(attrs={'class': 'form-check-input'}),
        method='filter_my_tasks',
    )

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'executor': ['exact'],
        }
        field_labels = {
            'status': _('Status'),
            'executor': _('Executor'),
        }
