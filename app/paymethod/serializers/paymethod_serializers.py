from django.db import transaction
from rest_framework.serializers import ModelSerializer

from paymethod.exceptions import PaymentMethodCreateBadRequestException, \
    PaymentMethodSettlementCycleCreateBadRequestException
from paymethod.models import PaymentMethodSettlementCycle, PaymentMethod


class PaymentMethodSettlementCycleSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethodSettlementCycle
        fields = '__all__'


class PaymentMethodSerializer(ModelSerializer):
    payment_method_settlement_cycles = PaymentMethodSettlementCycleSerializer(many=True, required=False)

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentMethodSettlementCycleCreateSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethodSettlementCycle
        field = [
            'cycle',
            'applied_date',
            'settlement_wait_time',
            'affiliate_withdrawal_use_or_not',
        ]


class PaymentMethodCreateSerializer(ModelSerializer):
    payment_method_settlement_cycles = PaymentMethodSettlementCycleCreateSerializer(many=True, required=False)

    class Meta:
        model = PaymentMethod
        fields = [
            'payment_method_settlement_cycles',
            'method_type',
            'service_use_or_not',
            'service_join_date',
            'store_type',
            'authentication_method',
            'partial_cancellation_or_not',
            'payment_use_or_not',
            'shipping_destination_use_or_not',
            'offline_cat_id',
            'card_information_save_use_or_not',
        ]

    @transaction.atomic()
    def create(self, validated_data):
        payment_method_settlement_cycles = validated_data.pop('payment_method_settlement_cycles')
        print(payment_method_settlement_cycles)
        try:
            # get_or_create 로 다시 만들기를 하였을 때 버그가 안나게 할 수 있지만
            # 일부러 업데이트 방향으로 이끌기 위해 버그를 만들어 주었다.
            payment_method = PaymentMethod.objects.get_or_create(
                paygouser=validated_data['paygouser'],
                method_type=validated_data.get('method_type', None),
                service_use_or_not=validated_data.get('service_use_or_not', None),
                service_join_date=validated_data.get('service_join_date', None),
                store_type=validated_data.get('store_type', None),
                authentication_method=validated_data.get('authentication_method', None),
                partial_cancellation_or_not=validated_data.get('partial_cancellation_or_not', None),
                payment_use_or_not=validated_data.get('payment_use_or_not', None),
                shipping_destination_use_or_not=validated_data.get('shipping_destination_use_or_not', None),
                offline_cat_id=validated_data.get('offline_cat_id', None),
                card_information_save_use_or_not=validated_data.get('card_information_save_use_or_not', None),
            )
        except Exception as e:
            print('결제 수단 테이블 만들때 에러', e)
            raise PaymentMethodCreateBadRequestException
        try:
            if payment_method_settlement_cycles:
                for payment_method_settlement_cycle in payment_method_settlement_cycles:
                    PaymentMethodSettlementCycle.objects.get_or_create(
                        cycle=payment_method_settlement_cycle['paygouser'],
                        applied_date=payment_method_settlement_cycle['applied_date'],
                        settlement_wait_time=payment_method_settlement_cycle.get('settlement_wait_time', None),
                        affiliate_withdrawal_use_or_not=payment_method_settlement_cycle.get(
                            'affiliate_withdrawal_use_or_not', None),
                        payment_method=payment_method,
                    )
        except Exception as e:
            print('결제 정산 주기 테이블 만들 때 에러', e)
            raise PaymentMethodSettlementCycleCreateBadRequestException
        return payment_method
