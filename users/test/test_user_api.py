from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')

VALID_EMAIL = 'test@gmail.com'
INVALID_EMAIL = 'testmail'
USERNAME = 'test'
VALID_PASSWORD = 'password'
INVALID_PASSWORD = 'pass'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
BIRTHDAY = '1996-10-29'


def create_user(**kwargs):
    email = kwargs.pop('email')
    password = kwargs.pop('password')
    return get_user_model().objects.create_user(email, password, **kwargs)


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

    def test_create_token_for_user(self):
        payload = {
            'email': VALID_EMAIL,
            'password': VALID_PASSWORD
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, data=payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(email='test@gmail.com', password='testpass')
        payload = {'email': 'wrong@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, data=payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_not_user(self):
        payload = {
            'email': VALID_EMAIL,
            'password': VALID_PASSWORD
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_required_fields(self):
        payload = {
            'email': VALID_EMAIL,
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUsersApiTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email=VALID_EMAIL, password=VALID_PASSWORD, first_name=FIRST_NAME)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(
            {'first_name': self.user.first_name, 'email': self.user.email}, res.data)

    def test_post_is_not_allowed_on_me_url(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'first_name': 'new_name', 'password': 'newpassword'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
