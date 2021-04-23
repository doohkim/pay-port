from django.contrib import admin

from members.models import PayGoUser
from payments.models import Payment
from datetime import timedelta


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'get_payed_at',

        'get_is_cancel',
        'represent_name',
        # 매체?
        # 결제 방식
        'paymethod',
        'status',
        'cancel_request_date',
        # 'card_name',
        # 'card_brand',
        'card_quota',
        'card_num',
        # 승인번호
        # 'approval_number',
        'is_canceled',
        'get_pg_return_date',
        'get_pg_return_propose_date',
        'price',
        'get_pg_fee_value',
        'get_pg_send_fund',
        'get_franchisee_return_fee',
        'get_franchisee_return_fund',
        'get_agency_return_fund',
        'buyer_name',

    )
    ordering = ('payed_at',)
    list_editable = ('status',)

    def get_payed_at(self, obj):
        payed_date = obj.payed_at.strftime('%Y-%m-%d %H:%M:%S')
        return payed_date

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

    def represent_name(self, obj):
        name = obj.paygouser.represent_name
        if name is not None:
            return name
        else:
            return '가맹점 이름 입력 해야함'

    def get_is_cancel(self, obj):
        if obj.is_canceled:
            return '취소'
        else:
            return '승인'

    def get_pg_return_date(self, obj):

        return_date = obj.payed_at + timedelta(days=3)
        return return_date

    def get_pg_return_propose_date(self, obj):
        return_date = obj.payed_at + timedelta(days=3)
        return_propose_date = return_date + timedelta(days=1)
        return return_propose_date

    def get_pg_fee_value(self, obj):
        pg_fee = obj.paygouser.agencies.agencies.agencies.settlement_informations.paygo_fee
        fee = obj.price * pg_fee / 100
        return fee

    def get_pg_send_fund(self, obj):
        pg_fee = obj.paygouser.agencies.agencies.agencies.settlement_informations.paygo_fee
        price = obj.price
        fee = price * pg_fee / 100
        send_fund = price - fee
        return send_fund

    def get_franchisee_return_fee(self, obj):
        agency = obj.paygouser.agencies
        pg_fee = agency.agencies.agencies.settlement_informations.paygo_fee
        agency_fee = agency.settlement_informations.agency_fee
        price = obj.price
        franchisee_fee = price * (pg_fee + agency_fee)  / 100
        return franchisee_fee

    def get_franchisee_return_fund(self, obj):
        agency = obj.paygouser.agencies
        pg_fee = agency.agencies.agencies.settlement_informations.paygo_fee
        agency_fee = agency.settlement_informations.agency_fee
        price = obj.price
        pg_fee = price * pg_fee / 100
        agency_fee = price * agency_fee / 100
        send_fund = price - pg_fee - agency_fee
        return send_fund

    def get_agency_return_fund(self, obj):
        agency = obj.paygouser.agencies
        agency_fee = agency.settlement_informations.agency_fee
        fee = obj.price * agency_fee / 100
        return fee

    def cancel_request_date(self, obj):
        if obj.status == 'cancel':
            canceled_date = obj.canceled_at.strftime('%Y-%m-%d %H:%M:%S')
            return canceled_date
        else:
            return None


    get_payed_at.short_description = '결제 시점'
    cancel_request_date.short_description = '취소 시점'
    account_number.short_description = '계좌번호'
    paymethod.short_description = '결제서비스'
    represent_name.short_description = '가맹점'
    get_is_cancel.short_description = '구분'
    get_pg_return_date.short_description = 'PG정산'


    get_pg_return_propose_date.short_description = '정산예정'
    get_pg_fee_value.short_description = 'PG사 수수료'
    get_pg_send_fund.short_description = 'PG입금'
    get_franchisee_return_fee.short_description = '가맹점수수료'
    get_franchisee_return_fund.short_description = '가맹점정산'
    get_agency_return_fund.short_description = '에이전트수수료'
