from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

# List 적당한 이름 찾기
from paymethod.models import PaymentMethod
from paymethod.serializers import PaymentMethodSerializer, PaymentMethodCreateSerializer


# class PaymentMethodListAPIView(ListAPIView):
#     permission_classes = [IsAuthenticated, ]
#     queryset = PaymentMethod.objects.all()
#     serializer_class = PaymentMethodSerializer
#
#
# class PaymentMethodCreateAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated, ]
#     queryset = PaymentMethod.objects.all()
#     serializer_class = PaymentMethodCreateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(paygouser=self.request.user)
#
