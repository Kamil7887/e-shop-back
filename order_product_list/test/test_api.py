from django.test import TestCase
from rest_framework.test import APIClient
from product.models import Product
from order.models import Order
from order_product_list.models import OrderProductList
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

LIST_CREATE_URL = reverse('order_product_list:list-create')
ORDER_LIST_CREATE_URL = reverse('order:list-create')
PRODUCT_LIST_CREATE_URL = reverse('product:list-create')


def RETRIEVE_UPDATE_DELETE_URL(order_id: int):
    return reverse('order_product_list:retrieve-update-delete', args=(order_id, ))


class TestPublicOrderProductListApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_list = []
        self.order_list = []
        self.product_list = []
        self.order_product_list = []
        self.superuser = get_user_model().objects.create_superuser(
            email='super@gmail.com', password='password')

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

    def test_create_order_product_list_fails(self):
        payload = {
            'order_id': self.order_list[0],
            'product_id': self.product_list[0],
            'amount': 1
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_order_product_list_fails(self):
        res = self.client.get(LIST_CREATE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_order_product_list_details_fails(self):
        res = self.client.get(RETRIEVE_UPDATE_DELETE_URL(
            order_id=self.order_list[1].id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_product_list_fails(self):
        res = self.client.delete(
            RETRIEVE_UPDATE_DELETE_URL(order_id=self.order_list[1].id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestPrivateOrderProductListApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_list = []
        self.order_list = []
        self.product_list = []
        self.order_product_list = []
        self.user1 = get_user_model().objects.create_user(
            email='user1@gmail.com', password='password')
        self.user2 = get_user_model().objects.create_user(
            email='user2@gmail.com', password='password')
        self.superuser = get_user_model().objects.create_superuser(
            email='super@gmail.com', password='password')

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

    def test_get_order_product_list(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(LIST_CREATE_URL)
        self.assertEqual(len(res.data), 0)

        order = self.client.post(ORDER_LIST_CREATE_URL, data={
            'user_id': self.user1.id})
        self.assertEqual(order.status_code, status.HTTP_201_CREATED)

        payload = {
            'order_id': order.data['id'],
            'product_id': self.product_list[0].id,
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            'order_id': order.data['id'],
            'product_id': self.product_list[1].id,
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            'order_id': order.data['id'],
            'product_id': self.product_list[2].id,
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        order = self.client.post(ORDER_LIST_CREATE_URL, data={
            'user_id': self.user1.id})
        self.assertEqual(order.status_code, status.HTTP_201_CREATED)

        payload = {
            'order_id': order.data['id'],
            'product_id': self.product_list[1].id,
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(LIST_CREATE_URL)
        self.assertEqual(len(res.data), 4)

    def test_create_order_product_list_item(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'order_id': self.order_list[0].id,
            'product_id': self.product_list[0].id,
        }
        res = self.client.post(LIST_CREATE_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['order_id'], self.order_list[0].id)

    def test_get_order_product_details_success(self):
        self.client.force_authenticate(self.user1)
        order_payload = {
            'user_id': self.user1.id
        }
        res_order_1 = self.client.post(
            ORDER_LIST_CREATE_URL, data=order_payload)
        self.assertEqual(res_order_1.status_code, status.HTTP_201_CREATED)

        order_product_payload = {
            'order_id': res_order_1.data['id'],
            'product_id': self.product_list[0].id
        }
        res_order_product = self.client.post(
            LIST_CREATE_URL, data=order_product_payload)
        self.assertEqual(res_order_product.status_code,
                         status.HTTP_201_CREATED)

        order_product_payload = {
            'order_id': res_order_1.data['id'],
            'product_id': self.product_list[1].id
        }
        res_order_product = self.client.post(
            LIST_CREATE_URL, data=order_product_payload)
        self.assertEqual(res_order_product.status_code,
                         status.HTTP_201_CREATED)

        order_payload = {
            'user_id': self.user1.id
        }
        res_order_2 = self.client.post(
            ORDER_LIST_CREATE_URL, data=order_payload)
        self.assertEqual(res_order_2.status_code, status.HTTP_201_CREATED)

        order_product_payload = {
            'order_id': res_order_2.data['id'],
            'product_id': self.product_list[3].id
        }
        res_order_product = self.client.post(
            LIST_CREATE_URL, data=order_product_payload)
        self.assertEqual(res_order_product.status_code,
                         status.HTTP_201_CREATED)

        res = self.client.get(RETRIEVE_UPDATE_DELETE_URL(
            order_id=res_order_1.data['id']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data[0])
        self.assertIsNotNone(res.data[1])
        self.assertEqual(len(res.data), 2)

    def test_order_id_and_product_id_fields_unique_together(self):
        self.client.force_authenticate(self.user1)
        order_payload = {
            'user_id': self.user1.id
        }
        res_order_1 = self.client.post(
            ORDER_LIST_CREATE_URL, data=order_payload)
        self.assertEqual(res_order_1.status_code, status.HTTP_201_CREATED)

        order_product_payload = {
            'order_id': res_order_1.data['id'],
            'product_id': self.product_list[0].id
        }
        res_order_product = self.client.post(
            LIST_CREATE_URL, data=order_product_payload)
        self.assertEqual(res_order_product.status_code,
                         status.HTTP_201_CREATED)
        res_order_product = self.client.post(
            LIST_CREATE_URL, data=order_product_payload)
        self.assertEqual(res_order_product.status_code,
                         status.HTTP_400_BAD_REQUEST)
