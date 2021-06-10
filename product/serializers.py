from product.models import Product
from rest_framework import fields, serializers
from transliterate import translit


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'slug', 'description',
                  'publisher', 'publication_date']
        extra_kwargs = {'slug': {'read_only': True}}

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product_id = product.id
        product_title = product.title
        slug = self.generate_slug(product_title, product_id)
        product.slug = slug
        product.save()
        return product

    def generate_slug(self, product_title: str, id: int):
        product_title = product_title.replace(' ', '-')
        product_title = translit(product_title, 'ru', reversed=True)
        slug = product_title+'-'+str(id)
        return slug
