from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80, required=True)
    last_name = serializers.CharField(max_length=80, required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=['MA', 'ST', 'ED','VI'])
    description = serializers.CharField(max_length=1000, required=False, default='')
    created_date = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()
    password = serializers.CharField(max_length=200)


class UserCreateUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=80, required=True)
    last_name = serializers.CharField(max_length=80, required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=['MA', 'ST', 'ED','VI'])
    description = serializers.CharField(max_length=1000, required=False, default='')
    password = serializers.CharField(required=True, max_length=200, allow_blank=False)

    def create(self, validated_data):
        pass
        print(validated_data)
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data['role'],
            description=validated_data['description'],
            password=make_password(validated_data['password']),
            username=validated_data['email']
        )
        user.save()
        return user