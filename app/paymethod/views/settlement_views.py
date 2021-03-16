from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from paymethod.models import SettlementInformation, SettlementAccount
from paymethod.serializers import SettlementInformationSerializer, SettlementInformationCreateSerializer, \
    SettlementInformationUpdateSerializer, SettlementAccountSerializer, SettlementAccountCreateSerializer


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


class SettlementInformationUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SettlementInformation.objects.all()
    serializer_class = SettlementInformationUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, paygouser=self.request.user)
        return obj


class SettlementInformationRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SettlementInformation.objects.all()
    serializer_class = SettlementInformationSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, paygouser=self.request.user)
        return obj


class SettlementAccountListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SettlementAccountSerializer

    def get_queryset(self):
        settle_info = SettlementInformation.objects.get(paygouser=self.request.user)
        queryset = settle_info.settlement_account.all()
        return queryset


class SettlementAccountCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SettlementAccountCreateSerializer
    queryset = SettlementAccount.objects.all()

    def perform_create(self, serializer):
        settle_info = SettlementInformation.objects.get(paygouser=self.request.user)
        serializer.save(settlement_information=settle_info)
