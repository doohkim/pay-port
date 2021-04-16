from django.contrib import admin

from members.models import PayGoUser
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'business_name',
        'paygo_user_email',
        'payed_at',
        'cancel_request_date',
        'price',
        'order_number',
        'paymethod',
        'is_canceled',
        'buyer_name',
        'goods_name',
        'account_number',
        'status',


    )
    ordering = ('payed_at',)
    list_editable = ('status',)

    def account_number(self, obj):
        settlement_info = obj.paygouser.settlement_informations.settlement_account.all()
        if settlement_info:
            recent_settlement_info = settlement_info[0]
            return recent_settlement_info.account_number
        return 'not Fount'

    def paymethod(self, obj):
        payment_method_info = obj.paygouser.payment_methods.all()
        if payment_method_info:
            recent_payment_method_info = payment_method_info[0]
            return recent_payment_method_info.method_type
        return 'not Fount'

    def business_name(self, obj):
        owner = obj.paygouser.owners
        if owner is not None:
            return obj.paygouser.owners.business_name
        else:
            return '입력해야해!'

    def cancel_request_date(self, obj):
        # created_datetime = obj.payed_at.strftime('%Y-%m-%d %H:%M:%S')
        # cancel_datetime = obj.canceled_at.strftime('%Y-%m-%d %H:%M:%S')
        if obj.status == 'cancel':
            return obj.canceled_at
        else:
            return

    def paygo_user_email(self, obj):
        user = obj.paygouser
        if user is not None:
            return obj.paygouser.email.split('@')[0]
        else:
            return None

    account_number.short_description = '계좌번호'
    paymethod.short_description = '결제서비스'
    business_name.short_description = '상호명'
    paygo_user_email.short_description = '유저 이메일'