from product.views import ListCreateProductView, RetrieveUpdateDestroyProductView
from django.urls import path

app_name = 'product'

urlpatterns = [
    path('', view=ListCreateProductView.as_view(), name='list-create'),
    path('<int:pk>', view=RetrieveUpdateDestroyProductView.as_view(),
         name='retrieve-update-delete'),
    # path('create/', view=CreateProductView.as_view(), name='create')
]
