from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from members.exceptions import PasswordNotMatchingException, TakenEmailException, LoginFailException
from members.models import PayGoUser


class SingUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = PayGoUser
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        if PayGoUser.objects.filter(email=data['email']).exists():
            raise TakenEmailException
        if data['password'] != data['password2']:
            raise PasswordNotMatchingException
        data.pop('password2')
        return data

    def create(self, validated_data):
        return PayGoUser.objects.create_user(**validated_data)


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGoUser
        fields = ['email', 'password']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise LoginFailException()

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email
            }
            return validation
        except PayGoUser.DoesNotExist:
            raise AuthenticationFailed()
