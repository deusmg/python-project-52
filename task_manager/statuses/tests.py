from django.test import TestCase
from task_manager.users.models import User
from task_manager.statuses.models import Status
from django.urls import reverse_lazy


class TestStatusCreate(TestCase):

    fixtures = ['statuses.json', 'users.json']

    def test_create_logout(self):
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_status(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.all().count(), 2)
        response = self.client.post(
            reverse_lazy('status_create'),
            {'name': 'status'}
        )
        self.assertEqual(Status.objects.all().count(), 3)


class TestUpdateStatus(TestCase):

    fixtures = ['statuses.json', 'users.json']

    def test_update_logout(self):
        response = self.client.get(reverse_lazy('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_status_update(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('status_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('status_update', kwargs={'pk': 1}),
            {'name': 'Started'}
        )
        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, 'Started')


class TestDeleteStatus(TestCase):

    fixtures = ['statuses.json', 'users.json']

    def test_delete_logout(self):
        response = self.client.get(reverse_lazy('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_delete_status(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('status_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 1})
        )
        statuses = Status.objects.all()
        self.assertEqual(len(statuses), 1)


class DeleteConnectedStatus(TestCase):

    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def test_delete_with_conn(self):
        user = User.objects.get(pk=1)
        status = Status.objects.get(pk=1)
        self.assertEqual(Status.objects.all().count(), 2)
        self.client.force_login(user=user)
        self.client.get(reverse_lazy('status_delete',
                        kwargs={'pk': status.id}))
        self.assertEqual(Status.objects.all().count(), 2)


class TestStatusesList(TestCase):

    fixtures = ['statuses.json', 'users.json']

    def test_list_logout(self):
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 302)

    def test_list_login(self):
        user = User.objects.get(pk=1)
        self.client.force_login(user=user)
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, 200)