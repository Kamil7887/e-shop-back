from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from order.models import Order
from product.models import Product
# Create your models here.


class OrderProductList(models.Model):
    class Meta:
        unique_together = (('order_id', 'product_id'),)

    order_id = ForeignKey(Order, related_name='order',
                          on_delete=models.CASCADE)
    product_id = ForeignKey(
        Product, related_name='product', on_delete=models.CASCADE)
    amount = IntegerField(default=1)

    def get_order_details(self, order: Order):
        return OrderProductList.objects.filter(order_id=order)
