from django.test import TestCase
from product.models import Product


class TestProductModel(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            title='title', description='desc')
        self.assertEqual(product.title, 'title')
