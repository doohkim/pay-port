from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

# List 적당한 이름 찾기
from paymethod.models import PaymentMethod, PaymentMethodSettlementCycle
from paymethod.serializers import PaymentMethodSerializer, PaymentMethodCreateSerializer, \
    PaymentMethodSettlementCycleCreateSerializer, PaymentMethodUpdateSerializer


class PaymentMethodListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class PaymentMethodCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodCreateSerializer

    def perform_create(self, serializer):
        print(self.request.user)
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


class PaymentMethodRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def get_object(self):
        # 신기하네 get 요청으로 데이터를 받네
        queryset = self.get_queryset()
        method_type = self.request.data['method_type']
        obj = get_object_or_404(queryset, paygouser=self.request.user, method_type=method_type)
        return obj
