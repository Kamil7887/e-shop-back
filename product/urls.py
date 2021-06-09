from product.views import CreateProductView
from django.urls import path

app_name = 'product'

urlpatterns = [
    path('create/', view=CreateProductView.as_view(), name='create')
]
