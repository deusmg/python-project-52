from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import activate

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskManagerTestCase(TestCase):

    fixtures = [
        'user/user.json',
        'status/status.json',
        'task/task.json',
        'label/label.json',
    ]

    login_url = reverse_lazy('login')
    logout_url = reverse_lazy('logout')

    users_url = reverse_lazy('users')
    statuses_url = reverse_lazy('statuses')
    tasks_url = reverse_lazy('tasks')
    labels_url = reverse_lazy('labels')

    activate('en')

    count = 3

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.bounded_user = User.objects.get(pk=2)
        self.another_user = User.objects.get(pk=3)
        self.status = Status.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.label = Label.objects.get(pk=1)
        self.client.force_login(self.user)
