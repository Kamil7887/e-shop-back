# Generated by Django 3.2.4 on 2021-06-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='was_paid',
            field=models.BooleanField(default=False),
        ),
    ]
