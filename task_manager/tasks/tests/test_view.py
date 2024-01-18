from task_manager.test_setup import TaskManagerTestCase


class TestStatusView(TaskManagerTestCase):

    def test_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_view_unauthenticated_with_flash(self):
        self.client.logout()
        response = self.client.get(self.tasks_url, follow=True)
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

    def test_success_view(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
