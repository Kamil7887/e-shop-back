from django.db.models import fields
from rest_framework import serializers
from order_product_list.models import OrderProductList
from order.serializers import OrderSerializer
from product.serializers import ProductSerializer


class OrderProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductList
        fields = ['id', 'order_id', 'product_id', 'amount']


class OrderProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProductList
        fields = ['id', 'order_id', 'product_id', 'amount']
        depth = 1
