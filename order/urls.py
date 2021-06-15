from order.views import ListCreateOrderView, RetrieveUpdateDestroyOrderView
from django.urls import path

app_name = 'order'

urlpatterns = [
    path('', view=ListCreateOrderView.as_view(), name='list-create'),
    path('<int:pk>', view=RetrieveUpdateDestroyOrderView.as_view(),
         name='retrieve-update-delete'),
]
