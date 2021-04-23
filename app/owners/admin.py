from django.contrib import admin

from members.models import PayGoUser
from owners.models import Owner, PayGoComputationalManager
import nested_admin


class ConnectPayGoUserManagerAdmin(nested_admin.NestedStackedInline):
    model = PayGoUser.franchisee_managers.through
    extra = 0


class ConnectOwnerManagerAdmin(nested_admin.NestedStackedInline):
    model = Owner.pay_managers.through
    extra = 0


@admin.register(Owner)
class OwnerAdmin(nested_admin.NestedModelAdmin):
    list_per_page = 20
    list_editable = ('contact_current_status',)
    list_display = (
        'id',
        'business_name',
        'business_license_number',
        'get_manager_name',
        # 'get_agencies',
        'business_representative_phone',
        'business_classification',
        'contact_current_status',
        'joined_date',
        # 수수료
        # 'buyer_name',
        # 원가 수수료
        # 'goods_name',
        # 대리점 수수료
        # 'account_number',
        # 총판 수수료
        # 'status',
        # 영중소 구분
        'contact_type',
    )
    ordering = ('joined_date',)
    # fieldsets = (
    #     ('가맹점 정보', {
    #         "fields": (
    #             'business_license_number', ('business_classification', 'business_name', ) , 'business_main_item',
    #             'application_route', 'sales_channel',
    #             ('business_store_type', 'business_condition'),
    #             'business_condition', 'business_capital_amount', 'business_url',
    #             'business_representative_name', 'business_representative_birth', 'corporate_registration_number',
    #             'business_representative_phone', 'business_representative_fax', 'business_representative_email',
    #             'transaction_amount', 'past_pg_company', 'business_official_address', 'business_real_address',
    #
    #
    #             ('business_type',),
    #             ('user_type', 'is_active')
    #         )
    #     }),
    #     ('가맹점 정보', {
    #         "fields": (("boss_name", "phone_number", "fax_number",),)
    #     }),
    #     ("사업자 등록", {
    #         "fields": ("owners",)
    #     }),
    #     ("에이전시 등록", {
    #         "fields": ("agencies",)
    #     }),
    #     ('기타 사항', {
    #         "fields": (
    #             ((
    #                  "transfer_or_not",
    #                  "published_or_not",
    #                  "pay_link_or_not",
    #                  "pg_info_auto_save_or_not",
    #                  "delivery_pay_or_not",
    #              ),)
    #         ),
    #     })
    # )
    inlines = (
        ConnectOwnerManagerAdmin,
    )

    def get_manager_name(self, obj):
        obj_bool = obj.owner_to_manager.exists()

        if obj_bool is True:
            connect_manager_obj = obj.owner_to_manager.all().order_by('-created_date').first()
            manager_name = connect_manager_obj.manager.name
            return manager_name
        else:
            return '매니저를 할당해주세요'

    def get_agencies(self, obj):
        user = obj.franchisee_to_agency
        if user is not None:
            email = user.email
            return email
        else:
            return '아이디가 없습니다'

    # user_email.short_description = '유저 ID'


@admin.register(PayGoComputationalManager)
class PayGoComputationalManagerAdmin(admin.ModelAdmin):
    pass
