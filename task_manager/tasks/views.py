from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.utils.translation import gettext as _

from ..mixins import UserAuthRequiredMixin, TaskAuthorPermissionMixin
from .models import Task
from .filters import TaskFilter
from .forms import TaskCreateForm, TaskUpdateForm


class TasksListView(UserAuthRequiredMixin, FilterView):
    template_name = 'tasks/task_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    permission_denied_message = _('You must to be log in')


class TaskView(UserAuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'

    login_url = reverse_lazy('login')

    permission_denied_message = _('You must to be log in')


class TaskCreateView(UserAuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'form.html'

    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    success_message = _('Task created successfully')
    permission_denied_message = _('You must to be log in')

    extra_context = {
        'header': _('Create task'),
        'button': _('Create'),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UserAuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'form.html'

    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    success_message = _('Task updated successfully')
    permission_denied_message = _('You must to be log in')

    extra_context = {
        'header': _('Update task'),
        'button': _('Update'),
    }


class TaskDeleteView(UserAuthRequiredMixin, SuccessMessageMixin,
                     TaskAuthorPermissionMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'

    login_url = reverse_lazy('login')
    success_url = reverse_lazy('tasks')
    author_url = success_url

    success_message = _('Task successfully removed')
    permission_denied_message = _('You must to be log in')
    author_message = _('Only its author can delete a task')
