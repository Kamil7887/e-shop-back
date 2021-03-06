# Generated by Django 3.2.4 on 2021-06-17 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_product_price'),
        ('order', '0002_alter_order_was_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProductList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'unique_together': {('order_id', 'product_id')},
            },
        ),
    ]
