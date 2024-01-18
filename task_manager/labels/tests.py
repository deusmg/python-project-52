from django.test import TestCase, Client
from django.urls import reverse_lazy
from http import HTTPStatus
from django.contrib.auth import get_user_model
from faker import Faker
from task_manager.labels.models import Label


User = get_user_model()

class LabelsTest(TestCase):
    """Test labels."""

    def setUp(self):
        """Create test user and label."""
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
        self.label = Label.objects.create(
            name=self.name,
        )
        self.label.save()

    def tearDown(self):
        """Teardown database."""
        self.user.delete()
        self.label.delete()

    def test(self):
        """Tests for labels."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse_lazy('labels'),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self._test_create_label()
        self._test_update_label(self.label)
        self._test_delete_label(self.label)

    def _test_create_label(self):
        response = self.client.post(
            reverse_lazy('label_create'),
            {'name': 'test label'},
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def _test_update_label(self, label):
        response = self.client.post(
            reverse_lazy(
                'label_update',
                args=(label.id,),
            ),
            {'name': 'test'},
        )
        changed_label = Label.objects.get(name='test')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(label.id, changed_label.id)

    def _test_delete_label(self, label):
        response = self.client.post(
            reverse_lazy(
                'label_delete',
                args=(label.id,),
            ),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=label.id)
