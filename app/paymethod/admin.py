import nested_admin
from django.contrib import admin

from paymethod.models import PaymentMethod, PaymentMethodSettlementCycle, SettlementInformation, SettlementAccount
import nested_admin


class PaymentMethodSettlementCycleInlineAdmin(nested_admin.NestedTabularInline):
    model = PaymentMethodSettlementCycle
    extra = 1


class PaymentMethodInlineAdmin(nested_admin.NestedTabularInline):
    model = PaymentMethod
    extra = 1
    inlines = (PaymentMethodSettlementCycleInlineAdmin,)


class SettlementAccountInlineAdmin(nested_admin.NestedTabularInline):
    model = SettlementAccount
    extra = 1


class SettlementInformationInlineAdmin(nested_admin.NestedTabularInline):
    model = SettlementInformation
    extra = 1
    inlines = (SettlementAccountInlineAdmin, )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    inlines = [PaymentMethodSettlementCycleInlineAdmin, ]


@admin.register(PaymentMethodSettlementCycle)
class PaymentMethodSettlementCycleAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementInformation)
class SettlementInformationAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementAccount)
class SettlementAccountAdmin(admin.ModelAdmin):
    pass
