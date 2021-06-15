from django.shortcuts import render
from rest_framework import generics, permissions, authentication
from order.models import Order
from order.serializers import OrderSerializer
# Create your views here.


class PostIfSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        if request.user.is_staff == True:
            return True
        else:
            return False


class ListCreateOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user_id=user.id)


class UpdateDeleteIfSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_staff:
            return True
        else:
            return False


class RetrieveUpdateDestroyOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated,
                          UpdateDeleteIfSuperuserPermission]

    def get_queryset(self):
        user = self.request.user
        if(user.is_superuser == True):
            return Order.objects.all()
        else:
            return Order.objects.filter(user_id=user.id)
