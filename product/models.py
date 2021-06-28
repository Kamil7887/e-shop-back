from django.db import models
import uuid
import os
# Create your models here.


def generate_product_image_file_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f'{uuid.uuid4}.{extension}'
    return os.path.join('product/images/', filename)


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.IntegerField()
    slug = models.SlugField(max_length=256, auto_created=True)
    description = models.TextField()
    publisher = models.CharField(max_length=128)
    publication_date = models.DateField(auto_now=True)
    image = models.ImageField(
        null=True, upload_to=generate_product_image_file_path)
