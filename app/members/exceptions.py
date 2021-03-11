from rest_framework import status
from rest_framework.exceptions import APIException


# Sign Up
class TakenEmailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 가입된 이메일 주소입니다.'
    default_code = 'TakenEmail'


class PasswordNotMatchingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'password1과 password2과 다릅니다.'
    default_code = 'PasswordNotMatching'


# Log In
class LoginFailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '로그인 실패 - email과 password를 확인해주세요.'
    default_code = 'LoginFail'



