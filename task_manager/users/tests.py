import json
from django.urls import reverse_lazy
from django.test import TestCase
from task_manager.users.models import User

with open('task_manager/fixtures/user.json') as file:
    new_user = json.loads(file.read())


class TestCreateUser(TestCase):

    def test_open_create_user(self):
        response = self.client.get(reverse_lazy('create'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_user(self):
        response = self.client.post(
            reverse_lazy('create'), new_user)
        self.assertRedirects(response, reverse_lazy('login'))
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, new_user.get('username'))
        self.assertEqual(User.objects.all().count(), 1)


class TestUpdateUser(TestCase):

    fixtures = ['users.json']

    def test_update_self_login(self):
        user = User.objects.get(pk=1)
        test_user = dict(new_user)
        self.client.force_login(user=user)
        response = self.client.post(reverse_lazy('update',
                                    kwargs={'pk': 1}), test_user)
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, new_user.get('username'))
        self.assertRedirects(response, reverse_lazy('users'))

    def test_update_not_self(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse_lazy('update', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))

    def test_update_logout(self):
        response = self.client.get(
            reverse_lazy('update', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteUserView(TestCase):

    fixtures = ['users.json']

    def test_delete_self(self):
        user = User.objects.get(pk=3)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse_lazy('delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')

    def test_delete_logout(self):
        response = self.client.get(
            reverse_lazy('delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_not_self(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(
            reverse_lazy('delete', kwargs={'pk': 2})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
