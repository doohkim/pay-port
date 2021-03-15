from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


class PaymentOrderNumberNotUniqueRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '주문번호가 이미 존재 합니다.'
    default_code = 'PaymentOrderNumber Error'


