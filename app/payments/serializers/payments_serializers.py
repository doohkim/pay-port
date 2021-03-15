from rest_framework.serializers import ModelSerializer

from members.serializers import UserDetailSerializer, serializers
from payments.exceptsions import PaymentOrderNumberNotUniqueRequestException
from payments.models import Payment


class PaymentSerializer(ModelSerializer):
    paygouser = UserDetailSerializer(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, attrs):
        print('validate', attrs)
        return attrs


class PaymentCreateSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'order_number',
            'goods_name',
            'card_num',
            'card_pwd',
            'card_avail_year',
            'card_avail_month',
            'price',
            'status',
            'card_quota',
            'buyer_name',
            'buyer_auth_num',
            'buyer_tel',
            'buyer_email',
            'is_canceled',
        )

    def validate(self, attrs):
        print('validate', attrs)
        obj = Payment.objects.filter(
            order_number=attrs['order_number']
        )
        if obj is not None:
            raise PaymentOrderNumberNotUniqueRequestException
        return attrs
