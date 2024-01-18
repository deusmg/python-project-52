from django.test import TestCase, Client
from django.urls import reverse_lazy
from http import HTTPStatus
from django.contrib.auth import get_user_model
from faker import Faker
from task_manager.statuses.models import Status


User = get_user_model()

class StatusesTest(TestCase):
    """Test statuses."""

    def setUp(self):
        """Create test user and status."""
        self.client = Client()
        self.faker = Faker()
        self.username = self.faker.user_name()
        self.password = self.faker.password(length=10)
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.user.save()
        self.name = self.faker.pystr()
        self.status = Status.objects.create(
            name=self.name,
        )
        self.status.save()

    def tearDown(self):
        """Teardown database."""
        self.user.delete()
        self.status.delete()

    def test(self):
        """Tests for statuses."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('statuses'),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self._test_create_status()
        self._test_update_status(self.status)
        self._test_delete_status(self.status)

    def _test_create_status(self):
        response = self.client.post(
            reverse_lazy('status_create'),
            {'name': 'testStatus'},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def _test_update_status(self, status):
        response = self.client.post(
            reverse_lazy(
                'status_update',
                args=(status.id,),
            ),
            {'name': 'test'},
        )
        changed_status = Status.objects.get(name='test')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(status.id, changed_status.id)

    def _test_delete_status(self, status):
        response = self.client.post(
            reverse_lazy(
                'status_delete',
                args=(status.id,),
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(status.DoesNotExist):
            Status.objects.get(pk=status.id)
