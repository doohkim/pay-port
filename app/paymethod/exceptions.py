from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


# 정산주기 serializer 실패
class SettlementAccountBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산계좌 serializer 데이터 Bad requests'
    default_code = 'Settlement Account'


class SettlementInformationCreateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산정보는 유저당 한개로 onetoone 관계이다.' \
                     '이미 정산정보가 있기 때문에 update 해주는 방향으로 가주십시오' \
                     'django.db.utils.IntegrityError: UNIQUE constraint failed:'
    default_code = 'Settlement Information Create'


class SettlementInformationUpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산정보는 업데이트 과정에서 에러남\n'
    default_code = 'Settlement Information Update'


class PaymentMethodCreateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제 수단 데이터 Create 에러'
    default_code = 'Payment Method Create'


class PaymentMethodSettlementCycleCreateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제 수단 정산 주기 Create 에러'
    default_code = 'Payment Method Create'


class PaymentMethodUpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제 수단 데이터 Update 에러'
    default_code = 'Payment Method Update'


class PaymentMethodSettlementCycleUpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제 수단 정산 주기 Update 에러'
    default_code = 'Payment Method Update'


class SettlementAccountListBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산정보-정산계좌 List API 정산계좌가 존재하지 않습니다. ' \
                     '정산정보에 정산계좌 정보를 만들어야 합니다.'
    default_code = 'SettlementAccount List'


class PaymentMethodSettlementCycleListBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '결제서비스 정보 API List API 정산주기가 존재하지 않습니다. ' \
                     '결제서비스 정보 안에  정산주기 정보를 만들어야 합니다.'
    default_code = 'PaymentMethodSettlementCycle List'
