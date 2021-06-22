from django.test import TestCase
from product.models import Product
from order.models import Order
from order_product_list.models import OrderProductList
from django.contrib.auth import get_user_model


class TestOrderProductListModel(TestCase):

    def setUp(self):
        self.user_list = []
        self.order_list = []
        self.product_list = []
        self.order_product_list = []

        for i in range(4):
            user = get_user_model().objects.create_user(
                email='test'+str(i)+'@gmail.com', password='password')
            self.user_list.append(user)

        for i in range(4):
            order = Order.objects.create(user_id=self.user_list[i])
            self.order_list.append(order)

        for i in range(4):
            product = Product.objects.create(
                title='title'+str(i), price=i*100, description='description'+str(i), publisher='publisher'+str(i))
            self.product_list.append(product)

        for order_index in range(1, 4):
            for product_index in range(1, 4):
                order_product_list_item = OrderProductList.objects.create(
                    order_id=self.order_list[order_index], product_id=self.product_list[product_index])
                self.order_product_list.append(order_product_list_item)

    def test_order_product_object_creation_success(self):
        op_list = OrderProductList.objects.create(
            order_id=self.order_list[0], product_id=self.product_list[0], amount=1)
        self.assertIsNotNone(op_list)
        self.assertEqual(op_list.order_id, self.order_list[0])
        self.assertEqual(op_list.product_id, self.product_list[0])
        self.assertEqual(op_list.amount, 1)
        op_list.delete()

    def test_default_amount_value_equals_one(self):
        op_list = OrderProductList.objects.create(
            order_id=self.order_list[0], product_id=self.product_list[0])
        self.assertEqual(op_list.amount, 1)
        op_list.delete()

    def test_duplicate_order_product_object_creation_fails(self):
        with self.assertRaises(BaseException):
            _ = OrderProductList.objects.create(
                order_id=self.order_list[1], product_id=self.product_list[1], amount=1)

    def test_get_order_details(self):
        order_details = OrderProductList.get_order_details(self,
                                                           order=self.order_list[1])
        self.assertEqual(len(order_details), 3)
        for item in order_details:
            self.assertEqual(item.order_id, self.order_list[1])
            self.assertEqual(item.amount, 1)
