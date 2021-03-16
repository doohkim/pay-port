from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

# List 적당한 이름 찾기
from members.models import PayGoUser
from paymethod.exceptions import PaymentMethodSettlementCycleListBadRequestException
from paymethod.models import PaymentMethod, PaymentMethodSettlementCycle
from paymethod.serializers import PaymentMethodSerializer, PaymentMethodCreateSerializer, \
    PaymentMethodSettlementCycleCreateSerializer, PaymentMethodUpdateSerializer, PaymentMethodSettlementCycleSerializer, \
    PaymentMethodSettlementCycleOnlySerializer, PaymentMethodOnlySerializer


class PaymentMethodListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentMethodCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodCreateSerializer

    def perform_create(self, serializer):
        serializer.save(paygouser=self.request.user)


class PaymentMethodUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()
        method_type = self.request.data['method_type']
        obj = get_object_or_404(queryset, paygouser=self.request.user, method_type=method_type)
        return obj


# 한 유저의 결제서비스 정보(수기, 신용카드, 가상계좌, ...등) 데이터
class PaymentMethodRetrieveAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        # 신기하네 get 요청으로 데이터를 받네
        queryset = PaymentMethod.objects.filter(paygouser=self.request.user)
        return queryset


# 결제서비스 중 한가지 방법(수기)의 정산 주기
class PaymentMethodSettlementCycleListAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def get_object(self):
        # 신기하네 get 요청으로도 json 데이터를 받네
        method_type = self.request.data['method_type']
        obj = get_object_or_404(self.get_queryset(), paygouser=self.request.user, method_type=method_type)
        return obj


class PaymentMethodSettlementCycleCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentMethodSettlementCycleCreateSerializer
    queryset = PaymentMethodSettlementCycle.objects.all()

    def perform_create(self, serializer):
        method_type = self.request.data['method_type']
        # method_type = '신용카드'
        payment_method_objest = PaymentMethod.objects.get(
            paygouser=self.request.user,
            method_type=method_type
        )
        # 명확히 어떤 결제서비스의 종류인지 보내줘야 함.

        serializer.save(payment_method=payment_method_objest)
