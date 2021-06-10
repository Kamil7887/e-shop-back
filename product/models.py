from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=256)
    price = models.IntegerField()
    slug = models.SlugField(max_length=256, auto_created=True)
    description = models.TextField()
    publisher = models.CharField(max_length=128)
    publication_date = models.DateField(auto_now=True)
