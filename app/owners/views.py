from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Owner, PayGoComputationalManager
from .serializers import OwnerSerializer, OwnerCreateSerializer


class OwnerListCreateAPIView(APIView):
    def get(self, request):
        owners = Owner.objects.all()
        data = OwnerSerializer(owners, many=True).data
        return Response(data)


class OwnerCreateView(generics.CreateAPIView):
    queryset = Owner.objects.get_queryset()
    serializer_class = OwnerCreateSerializer



# class ConnectCreateAPIView(APIView):

        # manager_raw_data = request.data.pop('paygocomputationmanagers')
        # manager_id_list = [manager["id"] for manager in manager_raw_data]
        # manager_list = PayGoComputationalManager.objects.filter(id__in=manager_id_list)
        # print(request.data)
# def post(self, request):
#     owner_data = request.data
#     print(owner_data)
#     serializer = OwnerSerializer(data=owner_data, many=True)
#     if serializer.is_valid():
#         serializer.save()
#         print(serializer.data)
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)
