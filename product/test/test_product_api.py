from django.core.exceptions import ValidationError
from django.test import TestCase, client
from rest_framework.test import APIClient
from product.models import Product
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

GET_PRODUCT_URL = reverse('product:list-create')
CREATE_PRODUCT_URL = reverse('product:list-create')

PRODUCT_TITLE = 'product title'
PRICE = 100000
RUSSIAN_PRODUCT_TITLE = 'название продукта'
PRODUCT_DESCRIPTION = 'long product description'
PUBLISHER = 'publisher'
VALID_PAYLOAD = {
    'title': PRODUCT_TITLE,
    'description': PRODUCT_DESCRIPTION,
    'publisher': PUBLISHER,
    'price': PRICE
}


class TestPublicProductApi(TestCase):
    def setUp(self):
        Product.objects.create(**VALID_PAYLOAD)
        Product.objects.create(**VALID_PAYLOAD)
        Product.objects.create(**VALID_PAYLOAD)

    def test_products_listed(self):
        res = self.client.get(GET_PRODUCT_URL)
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.data[0]['title'], PRODUCT_TITLE)


class TestPrivateProductApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        res = Product.objects.create(**VALID_PAYLOAD)
        self.prod_id = res.id
        self.not_staff_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='password')
        self.staff_user = get_user_model().objects.create_superuser(
            email='supertest@gmail.com', password='password'
        )

    def test_create_product_with_user_without_stuff_priveleges(self):
        payload = VALID_PAYLOAD
        self.client.force_authenticate(self.not_staff_user)
        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_success(self):
        payload = VALID_PAYLOAD
        self.client.force_authenticate(self.staff_user)
        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data['slug'])
        self.assertIsNotNone(res.data['publication_date'])

    def test_create_product_with_russian_title_success(self):
        payload = {
            'title': RUSSIAN_PRODUCT_TITLE,
            'description': PRODUCT_DESCRIPTION,
            'publisher': PUBLISHER,
            'price': PRICE
        }
        self.client.force_authenticate(self.staff_user)
        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data['slug'])

    def test_update_product_without_superuser_privelegies(self):
        self.client.force_authenticate(self.not_staff_user)
        payload = {
            'title': 'new title',
            'description': 'new description',
        }
        res = self.client.patch(
            reverse('product:retrieve-update-delete', args=(self.prod_id,)), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_product(self):
        self.client.force_authenticate(self.staff_user)
        _ = self.client.post(CREATE_PRODUCT_URL, VALID_PAYLOAD)
        res = self.client.post(CREATE_PRODUCT_URL, VALID_PAYLOAD)
        pk = res.data['id']
        self.client.logout
        res = self.client.get(
            reverse('product:retrieve-update-delete', args=(pk,)))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], VALID_PAYLOAD['title'])

    def test_update_product_with_superuser_privelegies(self):
        self.client.force_authenticate(self.staff_user)
        res = self.client.post(CREATE_PRODUCT_URL, VALID_PAYLOAD)
        pk = res.data['id']
        payload = {
            'title': 'new title',
            'description': 'new description',
        }
        self.assertIsNotNone(pk)
        res = self.client.patch(
            reverse('product:retrieve-update-delete', args=(pk,)), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], payload['title'])

    def test_update_non_existed_product(self):
        self.client.force_authenticate(self.staff_user)
        payload = {
            'title': 'new title',
            'description': 'new description',
        }
        res = self.client.patch(
            reverse('product:retrieve-update-delete', args=(1000,)), payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_with_not_staff_user(self):
        self.client.force_authenticate(self.not_staff_user)
        res = self.client.delete(
            reverse('product:retrieve-update-delete', args=(self.prod_id,)))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_with_staff_user(self):
        self.client.force_authenticate(self.staff_user)
        res = self.client.delete(
            reverse('product:retrieve-update-delete', args=(self.prod_id,)))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(
            reverse('product:retrieve-update-delete', args=(self.prod_id,)))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
