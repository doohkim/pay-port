from rest_framework.serializers import ModelSerializer

from paymethod.models import PaymentMethodSettlementCycle, PaymentMethod


class PaymentMethodSettlementCycleSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethodSettlementCycle
        fields = '__all__'


class PaymentMethodSerializer(ModelSerializer):
    paymentmethodsettlementcycles = PaymentMethodSettlementCycleSerializer(many=True, required=False)

    class Meta:
        model = PaymentMethod
        fields = '__all__'
