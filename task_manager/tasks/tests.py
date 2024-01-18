from django.test import TestCase, Client
from django.urls import reverse_lazy
from http import HTTPStatus
from django.contrib.auth import get_user_model
from faker import Faker
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


User = get_user_model()

class TasksTest(TestCase):
    """Test tasks."""

    def setUp(self):
        """Create test user and task."""
        self.client = Client()
        self.faker = Faker()
        self.username = self.faker.user_name()
        self.password = self.faker.password(length=10)
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.user.save()
        self.name = self.faker.pystr()
        self.status = Status.objects.create(
            name=self.faker.pystr()
        )
        self.task = Task.objects.create(
            name='test',
            executor=self.user,
            author=self.user,
            status=self.status,
        )
        self.task.save()

    def tearDown(self):
        """Teardown database."""
        self.task.delete()
        self.user.delete()
        self.status.delete()

    def test(self):
        """Tests for tasks."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('tasks'),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self._test_create_task()
        self._test_update_task(self.task)
        self._test_delete_task(self.task)

    def _test_create_task(self):
         response = self.client.post(
             reverse_lazy('task_create'),
             {'name': 'testTask',
             'status': self.status,
             'executor': self.user},
         )
         self.assertEqual(response.status_code, HTTPStatus.OK)

    def _test_update_task(self, task):
        response = self.client.post(
            reverse_lazy('task_update', args=(task.id,)),
            {'name': 'test'},
        )
        changed_task = Task.objects.get(id=task.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(changed_task.name, 'test')

    def _test_delete_task(self, task):
        response = self.client.post(
        reverse_lazy(
            'task_delete',
            args=(task.id,),
        ),
    )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=task.id)
