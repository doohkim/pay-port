from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentCreateSerializer, PaymentInfoSerializer


class PaymentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        serializer.save(paygouser=self.request.user)


class PaymentInfoListAPIView(ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = PaymentInfoSerializer
    queryset = Payment.objects.all()
