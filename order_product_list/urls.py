from django.urls import path
from order_product_list.views import ListCreateOrderProductListView, RetrieveOrderProductDetailsView
app_name = 'order_product_list'

urlpatterns = [
    path('', view=ListCreateOrderProductListView.as_view(), name='list-create'),
    path('<int:order_id>', view=RetrieveOrderProductDetailsView.as_view(),
         name='retrieve-update-delete'),
]
