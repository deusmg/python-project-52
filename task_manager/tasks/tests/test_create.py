from task_manager.test_setup import TaskManagerTestCase
from task_manager.json_loader import load_json
from ..models import Task

from django.urls import reverse_lazy


class TestTaskCreate(TaskManagerTestCase):

    create_url = reverse_lazy('task_create')
    created_cases = load_json('task/create.json')

    def test_success_create(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['valid']
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.tasks_url)
        self.assertEqual(Task.objects.count(), self.count + 1)

    def test_success_create_with_flash(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['valid'],
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'success')
        self.assertEqual(
            message.message,
            'Task created successfully'
        )
        self.assertTemplateUsed(
            response,
            'tasks/task_list.html'
        )

    def test_create_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            self.tasks_url,
            data=self.created_cases['valid']
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_unauthenticated_with_flash(self):
        self.client.logout()
        response = self.client.post(
            self.create_url,
            data=self.created_cases['valid'],
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'error')
        self.assertEqual(
            message.message,
            'You must to be log in'
        )
        self.assertTemplateUsed(response, 'form.html')

    def test_create_with_empty_name(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['empty_name']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_with_exist_name(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['already_exists']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)
