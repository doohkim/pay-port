from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


class BusinessLicenseNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '사업자등록번호가 유효하지 않습니다.'
    default_code = 'BusinessLicenseNumberE'


class NotFoundManagerNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '매니저 아이디 번호가 넘어오지 않았습니다.'
    default_code = 'client Not Foud Manager ID E'


class NotFoundMemoNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '메모 아이디 번호가 넘어오지 않았습니다.'
    default_code = 'client Not Foud Memo ID E'
