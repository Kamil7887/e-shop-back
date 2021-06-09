from product.serializers import ProductSerializer
from django.shortcuts import render
from product.models import Product
from rest_framework import generics


class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
