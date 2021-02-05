from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Owner, PayGoComputationalManager
from .serializers import OwnerSerializer, OwnerCreateSerializer


class OwnerListAPIView(APIView):
    # @staticmethod
    def get(self, request):
        owners = Owner.objects.all()
        data = OwnerSerializer(owners, many=True).data
        return Response(data)


class OwnerCreateView(generics.CreateAPIView):
    queryset = Owner.objects.get_queryset()
    serializer_class = OwnerCreateSerializer
