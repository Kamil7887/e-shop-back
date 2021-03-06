from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


def create_user(email, password, **kwargs):
    """
        required args: email,password;
        optional args: first_name,last_name,date_birthday
        """
    return get_user_model().objects.create_user(
        email=email, password=password, **kwargs)


class TestUser(TestCase):
    VALID_EMAIL = 'test@gmail.com'
    INVALID_EMAIL = 'testmail'
    USERNAME = 'test'
    VALID_PASSWORD = 'password'
    INVALID_PASSWORD = 'pass'

    def test_user_creation_with_email_and_password_pass(self):
        user = create_user(email=self.VALID_EMAIL,
                           password=self.VALID_PASSWORD)
        self.assertEqual(user.email, self.VALID_EMAIL)
        self.assertIsNotNone(user.password)

    def test_user_stored_password_is_hashed(self):
        user = create_user(email=self.VALID_EMAIL,
                           password=self.VALID_PASSWORD)
        self.assertNotEqual(user.password, self.VALID_PASSWORD)

    def test_user_creation_with_invalid_email_argument_fails(self):
        """
        email-value must match email pattern
        """
        with self.assertRaises(ValueError):
            _ = create_user(email=self.INVALID_EMAIL,
                            password=self.VALID_PASSWORD)

    def test_super_user_creation_pass(self):
        user = get_user_model().objects.create_superuser(
            email=self.VALID_EMAIL, password=self.VALID_PASSWORD)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_duplicate_user_creation_fails(self):
        _ = create_user(email=self.VALID_EMAIL,
                        password=self.VALID_PASSWORD)
        with self.assertRaises(IntegrityError):
            _ = create_user(email=self.VALID_EMAIL,
                            password=self.VALID_PASSWORD)

    def test_user_id_created(self):
        user = create_user(email=self.VALID_EMAIL,
                           password=self.VALID_PASSWORD)
        self.assertIsNotNone(user.id)
