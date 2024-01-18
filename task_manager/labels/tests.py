from django.test import TestCase
from task_manager.labels.models import Label
from task_manager.users.models import User
from django.urls import reverse_lazy


class TestLabelCreate(TestCase):

    fixtures = ['labels.json', 'users.json']

    def test_create_logout(self):
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_label(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.all().count(), 2)
        response = self.client.post(
            reverse_lazy('label_create'),
            {'name': 'label'}
        )
        self.assertEqual(Label.objects.all().count(), 3)


class TestUpdateLabel(TestCase):

    fixtures = ['labels.json', 'users.json']

    def test_update_logout(self):
        response = self.client.get(reverse_lazy('label_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_label_update(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('label_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 1}),
            {'name': 'Testing'}
        )
        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, 'Testing')


class TestDeleteLabel(TestCase):

    fixtures = ['labels.json', 'users.json']

    def test_delete_logout(self):
        response = self.client.get(reverse_lazy('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_delete_label(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('label_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 1})
        )
        labels = Label.objects.all()
        self.assertEqual(len(labels), 1)


class DeleteConnectedLabel(TestCase):

    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def test_delete_with_conn(self):
        label = Label.objects.get(pk=1)
        user = User.objects.get(pk=1)
        self.assertEqual(Label.objects.all().count(), 2)
        self.client.force_login(user=user)
        self.client.get(reverse_lazy('label_delete',
                        kwargs={'pk': label.id}))
        self.assertEqual(Label.objects.all().count(), 2)


class TestLabelsList(TestCase):

    fixtures = ['labels.json', 'users.json']

    def test_list_logout(self):
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, 302)

    def test_list__login(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, 200)