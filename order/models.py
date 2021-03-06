from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import BooleanField, DateField
from users.models import CustomUser
# Create your models here.


class Order(models.Model):
    """"
    user_id required
    order_date, was_paid autogenerated
    """
    user_id = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    order_date = DateField(auto_now=True, editable=False)
    was_paid = BooleanField(default=False)

    def get_user_orders(self, user: CustomUser):
        orders = Order.objects.filter(user_id=user.id)
        return orders
