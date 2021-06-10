from django.test import TestCase
from product.models import Product


class TestProductModel(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            title='title', description='desc', price='100')
        self.assertEqual(product.title, 'title')

    def test_id_field_created(self):
        product = Product.objects.create(
            title='title', description='desc', price='100')
        self.assertIsNotNone(product.id)
