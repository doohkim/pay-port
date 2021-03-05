from rest_framework import status, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Owner, PayGoComputationalManager
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

# class OwnerListAPIView(APIView):
#     # @staticmethod
#     def get(self, request):
#         owners = Owner.objects.all()
#         data = OwnerCreateSerializer(owners, many=True).data
#         return Response(data)
