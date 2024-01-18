from task_manager.test_setup import TaskManagerTestCase
from django.urls import reverse_lazy

from ..models import User


class TestUserDelete(TaskManagerTestCase):

    def test_user_delete_yourself(self):
        response = self.client.post(reverse_lazy('delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url)
        self.assertEqual(User.objects.count(), self.count - 1)

    def test_user_delete_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse_lazy('delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertEqual(User.objects.count(), self.count)

    def test_user_delete_another_user(self):
        response = self.client.post(reverse_lazy('delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_url)
        self.assertEqual(User.objects.count(), self.count)

    def test_delete_user_bounded_with_task(self):
        self.client.force_login(self.bounded_user)
        response = self.client.post(reverse_lazy(
            'delete', kwargs={'pk': 2}
        ), follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, 'error')
        self.assertEqual(
            message.message,
            'Cannot delete user because it is in use'
        )
        self.assertTemplateUsed(
            response,
            'users/user_list.html'
        )
