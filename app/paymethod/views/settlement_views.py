from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from paymethod.models import SettlementInformation
from paymethod.serializers import SettlementInformationSerializer, SettlementInformationCreateSerializer


class SettlementInformationListCreateAPIVew(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = SettlementInformation.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SettlementInformationSerializer
        elif self.request.method == 'POST':
            return SettlementInformationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(paygouser=self.request.user)
