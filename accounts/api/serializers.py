from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=20, min_length=8)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

        def validate(self, data):
            if User.objects.filter(username=data['usename'].lower()).exists():
                raise ValidationError({
                    'message': 'This username has been occupied.'
                })
            if User.objects.filter(email=data['email'].lower()).exists():
                raise ValidationError({
                    'message': 'This email address has been occupied.'
                })
            return data

        def create(self, validated_data):
            username = validated_data['username'].lower()
            password = validated_data['password']
            email = validated_data['email'].lower()

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return user
