from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.utils.translation import gettext as _
from django.conf import settings

from ..mixins import UserAuthRequiredMixin, TaskAuthorPermissionMixin
from .models import Task
from .filters import TaskFilter
from .forms import TaskCreateForm, TaskUpdateForm


class BaseTaskView(UserAuthRequiredMixin):
    login_url = reverse_lazy(getattr(settings, 'LOGIN_URL', 'login'))
    permission_denied_message = _('You must to be log in')


class TasksListView(BaseTaskView, FilterView):
    template_name = 'tasks/task_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskView(BaseTaskView, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(BaseTaskView, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task created successfully')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(BaseTaskView, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks')
    success_message = _('Task updated successfully')


class TaskDeleteView(BaseTaskView, SuccessMessageMixin, TaskAuthorPermissionMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    author_url = success_url
    success_message = _('Task successfully removed')
    author_message = _('Only its author can delete a task')
