from django.db.models.query import QuerySet
from rest_framework import generics, serializers
from order_product_list.serializers import OrderProductListSerializer, OrderProductDetailsSerializer
from rest_framework import authentication, permissions
from order_product_list.models import OrderProductList
from order.models import Order
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import response, status


class ListCreateOrderProductListView(generics.ListCreateAPIView):
    serializer_class = OrderProductListSerializer
    authentication = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        qs = Q()
        user = self.request.user
        user_orders = Order.get_user_orders(self, user=user)
        if(len(user_orders) <= 0):
            return OrderProductList.objects.none()
        else:
            for order in user_orders:
                qs = qs | Q(order_id=order)
            return OrderProductList.objects.filter(qs)


class RetrieveOrderProductDetailsView(generics.ListAPIView):
    serializer_class = OrderProductDetailsSerializer
    authentication = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'order_id'

    def get_queryset(self):
        qs = Q()
        user = self.request.user
        user_orders = Order.get_user_orders(self, user=user)
        if(len(user_orders) <= 0):
            return OrderProductList.objects.none()
        else:
            for order in user_orders:
                qs = qs | Q(order_id=order)
            return OrderProductList.objects.filter(qs)
    # def list(self, request, *args, **kwargs):
    #     order_id = kwargs['order_id']
    #     queryset = self.get_queryset()

    def list(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        queryset = self.get_queryset()
        queryset = queryset.filter(order_id=order_id)
        if(queryset.count == 0):
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
