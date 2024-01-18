from task_manager.test_setup import TaskManagerTestCase
from ..models import Status

from django.urls import reverse_lazy


class TestStatusDelete(TaskManagerTestCase):

    def test_status_delete_success(self):
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.statuses_url)
        self.assertEqual(Status.objects.count(), self.count - 1)

    def test_status_delete_success_with_flash(self):
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 3}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'success')
        self.assertEqual(
            message.message,
            'Status successfully removed'
        )
        self.assertTemplateUsed(
            response,
            'statuses/status_list.html'
        )

    def test_delete_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 2}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(Status.objects.count(), self.count)

    def test_delete_with_bounded_task(self):
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 1}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'error')
        self.assertEqual(
            message.message,
            'Cannot delete status because it is in use'
        )
        self.assertTemplateUsed(
            response,
            'statuses/status_list.html'
        )
