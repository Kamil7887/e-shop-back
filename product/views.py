from product.serializers import ProductSerializer
from product.models import Product
from rest_framework import generics, authentication, permissions


class PostIfSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        if request.user.is_staff == True:
            return True
        else:
            return False


class ListCreateProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [PostIfSuperuserPermission, ]


class UpdateDeleteIfSuperuserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_staff:
            return True
        else:
            return False


class RetrieveUpdateDestroyProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [UpdateDeleteIfSuperuserPermission, ]
