from django.urls import reverse_lazy

from task_manager.test_setup import TaskManagerTestCase
from task_manager.json_loader import load_json
from ..models import Label


class TestLabelCreate(TaskManagerTestCase):

    create_url = reverse_lazy('label_create')
    created_cases = load_json('label/create.json')

    def test_success_create(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['valid']
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)
        self.assertEqual(Label.objects.count(), 4)

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
            'Label created successfully'
        )
        self.assertTemplateUsed(
            response,
            'labels/label_list.html'
        )

    def test_create_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            self.labels_url,
            data=self.created_cases['valid']
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

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
        self.assertEqual(Label.objects.count(), 3)

    def test_create_with_exist_name(self):
        response = self.client.post(
            self.create_url,
            data=self.created_cases['already_exists']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 3)
