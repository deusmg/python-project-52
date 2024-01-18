from django.urls import reverse_lazy

from task_manager.test_setup import TaskManagerTestCase
from ..models import Label


class TestLabelDelete(TaskManagerTestCase):

    def test_delete_success(self):
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.labels_url)
        self.assertEqual(Label.objects.count(), 2)

    def test_delete_success_with_flash(self):
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'success')
        self.assertEqual(
            message.message,
            'Label successfully removed'
        )
        self.assertTemplateUsed(
            response,
            'labels/label_list.html'
        )

    def test_delete_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 2}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(Label.objects.count(), 3)

    def test_delete_with_bounded_task(self):
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 3)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'error')
        self.assertEqual(
            message.message,
            'Cannot delete label because it is in use'
        )
        self.assertTemplateUsed(
            response,
            'labels/label_list.html'
        )
