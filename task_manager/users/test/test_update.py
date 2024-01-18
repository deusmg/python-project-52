from task_manager.json_loader import load_json
from django.urls import reverse_lazy

from task_manager.test_setup import TaskManagerTestCase


class TestUserUpdate(TaskManagerTestCase):
    update_case = load_json('user/update.json')

    def test_user_update_view_authenticated(self):
        self.assertTrue(self.user.is_authenticated)
        response = self.client.post(reverse_lazy('update', kwargs={'pk': 1}),
                                    data=self.update_case)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.users_url)

    def test_user_update_view_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse_lazy('update', kwargs={'pk': 1}),
                                    data=self.update_case, follow=True)
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

    def test_user_update_without_permission(self):
        response = self.client.post(reverse_lazy('update', kwargs={'pk': 2}),
                                    data=self.update_case, follow=True)
        self.assertEqual(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'error')
        self.assertEqual(
            message.message,
            'You do not have permission to edit another user.'
        )
        self.assertTemplateUsed(response, 'users/user_list.html')
