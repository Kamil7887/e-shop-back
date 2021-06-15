from django.db.models import fields
from rest_framework import serializers
from order.models import Order
from django.contrib.auth import get_user_model


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_date', 'was_paid', ]

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
