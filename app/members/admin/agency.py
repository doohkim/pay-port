from django.contrib import admin

from members.admin import AgencyUserInline
from members.models import AgencyUser
from owners.admin import ConnectPayGoUserManagerAdmin
from paymethod.admin import SettlementInformationInlineAdmin, PaymentMethodInlineAdmin
import nested_admin

# agency를 manytomany로 잡아 줘야 할 수 도 있음
class AgencyUserAdmin(nested_admin.NestedModelAdmin):
    list_display = (
        'id',
        'store_joined_date',
        'get_business_name',
        'get_owner_number',
        'represent_name',
        'email',
        'business_type',
        'get_settlement_cycle',
        'get_total_fee',
        # 상태 추가
        'last_login',

    )
    fieldsets = (
        ('회원정보', {
            "fields": (('gid', 'mid_name'), 'email',
                       ('main_homepage', 'sub_homepage'),
                       ('business_type',),
                       ('user_type', 'is_active')
                       )
        }),
        ('가맹점 정보', {
            "fields": ("represent_name", "boss_name", "phone_number", "fax_number",)
        }),
        ("사업자 등록", {
            "fields": ("owners",)
        }),
        ("에이전시 등록", {
            "fields": ("agencies",)
        }),
        ('기타 사항', {
            "fields": (
                ((
                     "transfer_or_not",
                     "published_or_not",
                     "pay_link_or_not",
                     "pg_info_auto_save_or_not",
                     "delivery_pay_or_not",
                 ),)
            ),
        })
    )

    inlines = (
        ConnectPayGoUserManagerAdmin,
        PaymentMethodInlineAdmin,
        # AgencyUserInline,
        SettlementInformationInlineAdmin,
    )

    def get_owner_number(self, obj):
        if obj.owners is None:
            return 'not register'
        return obj.owners.business_license_number

    def get_business_name(self, obj):
        if obj.owners is None:
            return 'not register'
        return obj.owners.business_name

    def get_total_fee(self, obj):
        paygo_fee = obj.settlement_informations.paygo_fee
        agency_fee = obj.settlement_informations.agency_fee
        total_fee = paygo_fee + agency_fee
        return str(round(total_fee, 2)) + '%'

    def get_settlement_cycle(self, obj):
        pay_methods = obj.payment_methods.all()
        try:
            method_type = pay_methods.get(method_type='신용카드')
        except Exception as e:
            print(e)
            method_type = pay_methods.first()
        pay_method_settlement_info = method_type.payment_method_settlement_cycles.all().first()
        try:
            cycle = pay_method_settlement_info.cycle
            return cycle
        except Exception as e:
            print(e)
            cycle = None
            return cycle

    get_owner_number.short_description = '사업자번호'
    get_business_name.short_description = '상호명'
    get_total_fee.short_description = '전체 수수료'
    get_settlement_cycle.short_description = '정산주기'


admin.site.register(AgencyUser, AgencyUserAdmin)
