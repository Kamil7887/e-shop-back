import datetime
from django.test import TestCase
from order.models import Order
from django.contrib.auth import get_user_model


class TestOrderModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test1@gmail.com', password='password')

    def test_order_create_with_required_args_provided_success(self):
        order = Order.objects.create(user_id=self.user)
        self.assertIsNotNone(order)

    def test_that_orders_user_id_field_equal_to_users_id_field(self):
        order = Order.objects.create(user_id=self.user)
        self.assertEqual(order.user_id, self.user)

    def test_order_date_auto_create_success(self):
        order = Order.objects.create(user_id=self.user)
        self.assertIsNotNone(order.order_date)

    def test_order_auto_created_date_is_equal_to_current_date(self):
        now = datetime.date.today()
        order = Order.objects.create(user_id=self.user)
        self.assertEqual(order.order_date, now)

    def test_order_date_cant_be_modified(self):
        order = Order.objects.create(user_id=self.user)
        order.order_date = datetime.date(1996, 10, 29)
        order.save()
        self.assertNotEqual(order.order_date, datetime.date(1996, 10, 29))
        self.assertEqual(order.order_date, datetime.date.today())

    def test_order_is_paid_field_set_to_false_by_default(self):
        order = Order.objects.create(user_id=self.user)
        self.assertFalse(order.was_paid)

    def test_order_create_without_required_args_provided_fails(self):
        with self.assertRaises(BaseException):
            _ = Order.objects.create()

    def test_order_id_create_success(self):
        order = Order.objects.create(user_id=self.user)
        self.assertIsNotNone(order.id)

    def test_id_field_auto_increments_success(self):
        order1 = Order.objects.create(user_id=self.user)
        order2 = Order.objects.create(user_id=self.user)
        id_dif = order2.id-order1.id
        self.assertEqual(id_dif, 1)
