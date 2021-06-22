# Generated by Django 3.2.4 on 2021-06-22 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_was_paid'),
        ('product', '0004_product_image'),
        ('order_product_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproductlist',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='order.order'),
        ),
        migrations.AlterField(
            model_name='orderproductlist',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='product.product'),
        ),
    ]
