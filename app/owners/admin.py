from django.contrib import admin

from members.models import PayGoUser
from owners.models import Owner, PayGoComputationalManager
import nested_admin


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_per_page = 20
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
    list_editable = ('contact_current_status',)

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


class ConnectPayGoUserManagerAdmin(nested_admin.NestedStackedInline):
    model = PayGoUser.franchisee_managers.through
    extra = 0
