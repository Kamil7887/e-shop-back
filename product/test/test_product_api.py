from django.test import TestCase, client
from rest_framework.test import APIClient
from product.models import Product
from django.urls import reverse
from rest_framework import status

CREATE_PRODUCT_URL = reverse('product:create')

PRODUCT_TITLE = 'product title'
RUSSIAN_PRODUCT_TITLE = 'название продукта'
PRODUCT_DESCRIPTION = 'long product description'
PUBLISHER = 'publisher'


class TestProductApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_product_success(self):
        payload = {
            'title': PRODUCT_TITLE,
            'description': PRODUCT_DESCRIPTION,
            'publisher': PUBLISHER,
        }
        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data['slug'])
        self.assertIsNotNone(res.data['publication_date'])

    def test_create_product_with_russian_title_success(self):
        payload = {
            'title': RUSSIAN_PRODUCT_TITLE,
            'description': PRODUCT_DESCRIPTION,
            'publisher': PUBLISHER,
        }
        res = self.client.post(CREATE_PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data['slug'])
