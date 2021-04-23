from django.contrib import admin

from members.models import FranchiseeUser, AgencyUser

import nested_admin

from owners.admin import ConnectPayGoUserManagerAdmin
from paymethod.admin import PaymentMethodInlineAdmin, SettlementInformationInlineAdmin


@admin.register(FranchiseeUser)
class FranchiseeUserAdmin(nested_admin.NestedModelAdmin):
    fieldsets = (
        ('회원정보', {
            "fields": (('gid', 'mid_name'), 'email', ('main_homepage', 'sub_homepage'), ('business_type',),
                       ('user_type', 'is_active')
                       )
        }),
        ('가맹점 정보', {
            "fields": (("represent_name", "boss_name", "phone_number", "fax_number",),)
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
        # 에이전시 등록 기존에 걸로 등록 할수 있는게 좋겠다 싶어 여기는 이렇게 열어놈
        # AgencyUserInline,
        SettlementInformationInlineAdmin,
    )
    list_display = (
        'id',
        'get_owner_number',
        'represent_name',
        'email',
        'business_type',
        'phone_number',
        'store_joined_date',

        # 대리점
        'get_direct_agency',
        'get_direct_agency_fee',
        # 총판
        'get_distributor',
        'get_distributor_fee',
        # # 지사
        'get_branch',
        'get_branch_fee',

        # 영중소 구분(무엇?)

    )

    def get_owner_number(self, obj):
        if obj.owners is None:
            return 'not register'
        return obj.owners.business_license_number

    def get_business_name(self, obj):
        if obj.owners is None:
            return 'not register'
        return obj.owners.business_name

    def get_direct_agency(self, obj):
        if obj.agencies is None:
            # obj.agencies = AgencyUser.objects.get(email='lumen_bottom@gmail.com')
            obj.agencies = AgencyUser.objects.first()
            return obj.agencies.represent_name
        return obj.agencies.represent_name

    def get_direct_agency_fee(self, obj):
        # 대리점 에이전트
        agency = obj.agencies
        # 총판 에이전트 수수료
        distributor_fee = agency.agencies.settlement_informations.agency_fee
        # 대리점 is None 이면
        if agency is None:
            # obj.agencies = AgencyUser.objects.get(email='lumen_bottom@gmail.com')
            # 가맹점 대리점을 우리 루멘 대리점으로 등록한다
            agency = AgencyUser.objects.first()
            # 루멘 총판 이름
            name = agency.represent_name
            # 루멘 대리점 수수료
            agency_fee = agency.settlement_informations.agency_fee
        else:
            # 총판이름
            name = agency.represent_name
            # 총판 수수료
            agency_fee = agency.settlement_informations.agency_fee

        if agency_fee < distributor_fee:
            return f'{name}수수료 {distributor_fee}보다 높게 수정'
        return str(round(agency_fee, 2)) + '%'

    def get_distributor(self, obj):
        if obj.agencies.agencies is None:
            # obj.agencies = AgencyUser.objects.get(email='lumen_middle@gmail.com')
            obj.agencies.agencies = AgencyUser.objects.get(id=6)
            return obj.agencies.agencies.represent_name
        return obj.agencies.agencies.represent_name

    def get_distributor_fee(self, obj):
        # 총판 에이전트
        agency = obj.agencies.agencies
        # 지사 에이전트 수수료
        branch_fee = agency.agencies.settlement_informations.agency_fee
        # 총판 is None 이면
        if agency is None:
            # obj.agencies = AgencyUser.objects.get(email='lumen_middle@gmail.com')
            # 가맹점 총판을 루멘 총판으로 등록한다
            agency = AgencyUser.objects.get(id=6)
            # 루멘 총판 이름
            name = agency.represent_name
            # 루맨 총판 수수료
            fee = agency.settlement_informations.agency_fee
            # return str(round(fee, 2)) + '%'
        # 총판이 존재하면
        else:
            # 총판이름
            name = agency.represent_name
            # 총판 수수료
            fee = agency.settlement_informations.agency_fee
        if fee < branch_fee:
            return f'{name}수수료 {branch_fee}보다 높게 수정'
        else:
            return str(round(fee, 2)) + '%'

    def get_branch(self, obj):
        if obj.agencies.agencies.agencies.represent_name == obj.agencies.agencies.agencies.agencies.represent_name:
            obj.agencies.agencies.agencies.agencies = None
        if obj.agencies.agencies.agencies is None:
            obj.agencies.agencies.agencies = AgencyUser.objects.get(email='lumen_top@gmail.com')
            return obj.agencies.agencies.agencies.represent_name
        return obj.agencies.agencies.agencies.represent_name

    def get_branch_fee(self, obj):
        # if obj.agencies.agencies.agencies.represent_name == obj.agencies.agencies.agencies.agencies.represent_name:
        #     obj.agencies.agencies.agencies.agencies = None
        if obj.agencies.agencies.agencies is None:
            obj.agencies.agencies.agencies = AgencyUser.objects.get(email='lumen_top@gmail.com')
            fee = obj.agencies.agencies.agencies.settlement_informations.agency_fee
            return str(round(fee, 2)) + '%'
        fee = obj.agencies.agencies.agencies.settlement_informations.agency_fee
        return str(round(fee, 2)) + '%'

    get_owner_number.short_description = '사업자번호'
    get_business_name.short_description = '상호명'
    get_direct_agency.short_description = '대리점'
    get_distributor.short_description = '총판'
    get_branch.short_description = '지사'
    get_direct_agency_fee.short_description = '대리점 수수료'
    get_distributor_fee.short_description = '총판 수수료'
    get_branch_fee.short_description = '지사 수수료'
