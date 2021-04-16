from rest_framework.serializers import ModelSerializer

from members.models import PayGoUser
from members.serializers import UserDetailSerializer, serializers, UserPaymentInfoDetailSerializer
from payments.exceptsions import PaymentOrderNumberNotUniqueRequestException
from payments.models import Payment
from paymethod.serializers import PaymentMethodSerializer


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
        obj = Payment.objects.filter(
            order_number=attrs['order_number']
        )
        print('obj', len(obj) )
        print(attrs['order_number'])
        if len(obj) != 0:
            raise PaymentOrderNumberNotUniqueRequestException
        return attrs


class PaymentInfoSerializer(ModelSerializer):
    paygouser = UserPaymentInfoDetailSerializer(required=False, read_only=True)


    class Meta:
        model = Payment
        fields = "__all__"

    # def get_pay_method_info(self, obj):
