from django.db.models import fields
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    fields = ['user_id', ]
