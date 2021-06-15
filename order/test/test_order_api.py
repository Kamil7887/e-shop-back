from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from order.models import Order


LIST_CREATE_ORDER_URL = reverse('order:list-create')
CREATE_USER_URL = reverse('users:create')


def genereate_rud_order_url(id: int):
    return reverse('order:retrieve-update-delete', args=(id,))


def generate_user_payload(index: int):
    return {
        'email': 'test' + str(index) + '@gmail.com',
        'password': 'password'
    }


class TestPublicOrderApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.users_id = []
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com', password='password')
        self.users_id.append(self.user.id)
        self.super_user = get_user_model().objects.create_superuser(
            email='superuser@gmail.com', password='password')
        self.users_id.append(self.super_user.id)

    def test_get_order_list_unauthorized_requests_fails(self):
        res_list = self.client.get(LIST_CREATE_ORDER_URL)
        self.assertEqual(res_list.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_post_order_fails(self):
        payload = {
            'user_id': self.users_id[0]
        }
        res = self.client.post(LIST_CREATE_ORDER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_retrieve_order_fails(self):
        self.client.force_authenticate(user=self.user)
        res_order = self.client.post(LIST_CREATE_ORDER_URL, {
                                     'user_id': self.user.id, })
        self.assertEqual(res_order.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        res_get = self.client.get(
            genereate_rud_order_url(res_order.data['id']))
        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_order_fails(self):
        self.client.force_authenticate(self.user)

        res_order = self.client.post(LIST_CREATE_ORDER_URL, {
                                     'user_id': self.user.id})
        self.assertEqual(res_order.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        payload = {
            'was_paid': True
        }
        res_post = self.client.post(
            genereate_rud_order_url(res_order.data['id']), payload)
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete_order_fails(self):
        self.client.force_authenticate(self.user)
        res_order = self.client.post(LIST_CREATE_ORDER_URL, {
                                     'user_id': self.user.id})
        self.assertEqual(res_order.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        res_post = self.client.delete(
            genereate_rud_order_url(res_order.data['id']))
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateOrderApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.users_id = []
        self.orders_id = []
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com', password='password')
        self.users_id.append(self.user.id)
        self.super_user = get_user_model().objects.create_superuser(
            email='superuser@gmail.com', password='password')
        self.users_id.append(self.super_user.id)
        self.client.force_authenticate(self.user)
        self.client.post(LIST_CREATE_ORDER_URL, data={
                         'user_id': self.users_id[0]})
        self.client.post(LIST_CREATE_ORDER_URL, data={
                         'user_id': self.users_id[1]})
        self.client.logout()

    def test_authorized_order_list_request_success(self):
        self.client.force_authenticate(self.user)
        res_list = self.client.get(LIST_CREATE_ORDER_URL)
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(res_list.data), Order.objects.count())
        for i in res_list.data:
            self.assertNotEqual(i['user_id'], self.super_user.id)

    def test_authorized_order_create_request_success(self):
        self.client.force_authenticate(self.user)
        res_create = self.client.post(LIST_CREATE_ORDER_URL, {
                                      'user_id': self.user.id})
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)

    def test_authorized_get_order_details_of_this_user_success(self):
        self.client.force_authenticate(self.user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.user.id})
        order_id = res_post.data['id']
        res_get = self.client.get(genereate_rud_order_url(order_id))
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)

    def test_authorized_get_order_details_of_different_user_fails(self):
        self.client.force_authenticate(self.user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.super_user.id})
        order_id = res_post.data['id']
        res_get = self.client.get(genereate_rud_order_url(order_id))
        self.assertEqual(res_get.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_order_update_requst_with_superuser_priveleges_success(self):
        self.client.force_authenticate(self.super_user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.user.id})
        order_id = res_post.data['id']
        payload = {'was_paid': True}
        res_update = self.client.patch(
            genereate_rud_order_url(order_id), payload)
        self.assertEqual(res_update.status_code, status.HTTP_200_OK)

    def test_authorized_order_update_reqeust_without_superuser_priveleges_fails(self):
        self.client.force_authenticate(self.user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.user.id})
        order_id = res_post.data['id']
        payload = {'was_paid': True}
        res_update = self.client.patch(
            genereate_rud_order_url(order_id), payload)
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_order_delete_request_without_superuser_priveleges_fails(self):
        self.client.force_authenticate(self.user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.user.id})
        order_id = res_post.data['id']
        res_delete = self.client.delete(genereate_rud_order_url(order_id))
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_order_delete_request_with_superuser_priveleges_fails(self):
        self.client.force_authenticate(self.super_user)
        res_post = self.client.post(
            LIST_CREATE_ORDER_URL, {'user_id': self.user.id})
        order_id = res_post.data['id']
        res_delete = self.client.delete(genereate_rud_order_url(order_id))
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
