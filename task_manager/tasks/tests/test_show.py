from task_manager.test_setup import TaskManagerTestCase
from django.urls import reverse_lazy


class TestTaskShow(TaskManagerTestCase):

    def test_success_show(self):
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/show.html')

    def test_show_unauthenticated(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_show_unauthenticated_with_flash(self):
        self.client.logout()
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 1}),
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
