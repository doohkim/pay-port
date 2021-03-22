from datetime import timedelta, datetime

import requests

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import PayGoUser
from members.serializers.user_serializers import SingUpSerializer, AuthSerializer, UserLoginSerializer, \
    UserDetailSerializer, RegisterSerializer


class SignUpAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = PayGoUser.objects.all()
    serializer_class = SingUpSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = PayGoUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)


class AuthTokenAPIVIew(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        # print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            return AuthenticationFailed()
        return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class AuthUserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            status_code = status.HTTP_200_OK
            url = 'http://13.125.1.183/api/token/refresh/'
            data = {
                "refresh": serializer.data['refresh']
            }
            res = requests.post(url, data=data)
            refresh_access_token = res.json()
            print(serializer.data)
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    # 'id': serializer.data['id'],
                    'email': serializer.data['email'],
                    'refresh_access_token': refresh_access_token,
                    # 'time': datetime.now()
                }
            }
            return Response(response, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class TokenSendEmailAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        email = request.data['email']
        print(email)
        if email is not None:
            subject = '[pay-port] 계정 비밀번호 변경 링크'
            message = f'http://127.0.0.1:8000/api/token/refresh/?accesstoken={request.auth.token}'
            mail = EmailMessage(subject, message, to=[email])
            mail.send()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PwdResetEmailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        password = request.data['password']
        request.user.set_password(password)
        request.user.save()
        content = {
            'status': 'password changed success'
        }
        return Response(content, status=status.HTTP_200_OK)


class UserLogoutAPIView(generics.GenericAPIView):
    pass


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PayGoUser.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj



class HelloView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
