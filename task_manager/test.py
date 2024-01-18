from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate
from task_manager.users.models import User


class IndexTest(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class SigninTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='12test12')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)
