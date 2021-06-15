from django.shortcuts import render
from rest_framework import generics, permissions, authentication
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
    pass
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # authentication_classes = [authentication.TokenAuthentication, ]
    # permission_classes = [PostIfSuperuserPermission, ]


class UpdateDeleteIfSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_staff:
            return True
        else:
            return False


class RetrieveUpdateDestroyOrderView(generics.RetrieveUpdateDestroyAPIView):
    pass
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # authentication_classes = [authentication.TokenAuthentication, ]
    # permission_classes = [UpdateDeleteIfSuperuserPermission, ]
