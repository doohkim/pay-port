import requests

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from members.exceptions import LoginFailException
from members.models import PayGoUser
from members.serializers.user_serializers import AuthSerializer, UserLoginSerializer, \
    UserDetailSerializer, RegisterSerializer


class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = PayGoUser.objects.all()

    def post(self, request):
        email = request.data['username']
        password = request.data['password']
        data = {
            "email": email,
            "password": password
        }
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

        else:
            return LoginFailException
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            return LoginFailException()
        data = {
            'token': token.key,
            'email': user.email,
            'username': user.email.split('@')[0]
        }
        return Response(data=data, status=status.HTTP_200_OK)


# 로그인 정보
class AuthTokenAPIVIew(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request):
        email = request.data['username']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            return LoginFailException()
        data = {
            'token': token.key,
            'email': user.email,
            'username': user.email.split('@')[0]
        }
        return Response(data=data, status=status.HTTP_200_OK)


class AuthUserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # url = 'http://13.125.1.183/api/token/refresh/'
            # data = {
            #     "refresh": serializer.data['refresh']
            # }
            # res = requests.post(url, data=data)
            # refresh_access_token = res.json()
            response = {
                'success': True,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'email': serializer.data['email'],
            }
            return Response(response, status=status.HTTP_200_OK)
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
    permission_classes = (AllowAny,)
    queryset = Token.objects.all()

    def post(self, request):
        queryset = self.get_queryset()
        user_token = request.data['userToken']
        if user_token:
            token = queryset.get(key=user_token)
        else:
            return AuthenticationFailed()
        token.delete()
        return Response('logout success', status=status.HTTP_204_NO_CONTENT)


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PayGoUser.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj

#
# class UserTokenTestAPIView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = PayGoUser.objects.all()
#     serializer_class = UserDetailSerializer
#
#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, email=self.request.data['email'])
#         return obj
#
#     def post(self, request):
#         serializer = self.serializer_class(self.get_object())
#         return Response(serializer.data)
