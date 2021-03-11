from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError


# 정산주기 serializer 실패
class SettlementAccountBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산계좌 serializer 데이터 Bad requests'
    default_code = 'Settlement Account'


class SettlementInformationBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '정산정보는 유저당 한개로 onetoone 관계이다.\n 이미 정산정보가 있기 때문에 update 해주는 방향으로 가주십시오\ndjango.db.utils.IntegrityError: UNIQUE constraint failed:'
    default_code = 'Settlement Information'
