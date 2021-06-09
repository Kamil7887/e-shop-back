from rest_framework import fields, serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name', 'date_birthday']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        return get_user_model().objects.create_user(email=email, password=password, **validated_data)
