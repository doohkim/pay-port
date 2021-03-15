from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common import check_owner_number

from .excepts import BusinessLicenseNumberException
from .models import Owner
from .serializers import OwnerSerializer


class OwnerLIstCreateView(generics.ListCreateAPIView):
    queryset = Owner.objects.get_queryset()
    serializer_class = OwnerSerializer


class OwnerUpdateView(generics.UpdateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

    def get_object(self):
        queryset = self.get_queryset()
        lookup_field = self.request.data['business_license_number']
        obj = get_object_or_404(queryset, business_license_number=lookup_field)
        return obj


class OwnerNumberCheckView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        business_license_number = request.data['business_license_number']
        result, boolean_result = check_owner_number(business_license_number)
        data = {}
        if boolean_result:
            # 모델에 데이터 필드 추가하기
            data['call_contents'] = result
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise BusinessLicenseNumberException

# class OwnerListAPIView(APIView):
#     # @staticmethod
#     def get(self, request):
#         owners = Owner.objects.all()
#         data = OwnerCreateSerializer(owners, many=True).data
#         return Response(data)
