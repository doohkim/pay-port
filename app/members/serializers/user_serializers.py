from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from members.exceptions import TakenEmailException, LoginFailException
from members.models import PayGoUser
from owners.serializers import OwnerSerializer
from paymethod.serializers import SettlementInformationSerializer, PaymentMethodSerializer


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = PayGoUser
        fields = ['email', 'password', ]

    def validate(self, data):
        if PayGoUser.objects.filter(email=data['email']).exists():
            raise TakenEmailException
        return data

    def create(self, validated_data):
        # print(validated_data)
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
                'email': user.email,
                'id': user.id
            }
            return validation
        except PayGoUser.DoesNotExist:
            raise AuthenticationFailed()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGoUser
        exclude = [
            'password',
        ]


class UserPaymentInfoDetailSerializer(serializers.ModelSerializer):
    settlement_informations = SettlementInformationSerializer()
    payment_methods = PaymentMethodSerializer(many=True)
    owners = OwnerSerializer()
    class Meta:
        model = PayGoUser
        exclude = [
            'password',
        ]

# 비밀번호 두개 받을때
# class SingUpSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = PayGoUser
#         fields = ['email', 'password', 'password2']
#
#     def validate(self, data):
#         print(data)
#         if PayGoUser.objects.filter(email=data['email']).exists():
#             raise TakenEmailException
#         if data['password'] != data['password2']:
#             raise PasswordNotMatchingException
#         data.pop('password2')
#         return data
#
#     def create(self, validated_data):
#         print(validated_data)
#         return PayGoUser.objects.create_user(**validated_data)
