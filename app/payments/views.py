from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer, PaymentCreateSerializer


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