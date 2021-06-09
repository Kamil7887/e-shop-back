from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.serializers import UserSerializer

CREATE_USER_URL = reverse('user:create')
VALID_EMAIL = 'test@gmail.com'
INVALID_EMAIL = 'testmail'
USERNAME = 'test'
VALID_PASSWORD = 'password'
INVALID_PASSWORD = 'pass'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
BIRTHDAY = '29-10-1996'


def create_user(email, password, **kwargs):
    """
        required args: email,password;
        optional args: first_name,last_name,date_birthday
        """
    return get_user_model().objects.create_user(
        email=email, password=password, **kwargs)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': VALID_EMAIL,
            'password': VALID_PASSWORD,
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'date_birthday': BIRTHDAY}
        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        payload = {
            'email': VALID_EMAIL,
            'password': VALID_PASSWORD,
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'date_birthday': BIRTHDAY}
        self.client.post(CREATE_USER_URL, data=payload)
        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        payload = {
            'email': VALID_EMAIL,
            'password': INVALID_PASSWORD,
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'date_birthday': BIRTHDAY}
        res = self.client.post(CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(**payload).exists()
        self.assertFalse(user_exist)
