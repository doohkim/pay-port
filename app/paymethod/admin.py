import nested_admin
from django.contrib import admin

from paymethod.models import PaymentMethod, PaymentMethodSettlementCycle, SettlementInformation, SettlementAccount
import nested_admin


class PaymentMethodSettlementCycleInlineAdmin(nested_admin.NestedStackedInline):
    model = PaymentMethodSettlementCycle
    extra = 0


class PaymentMethodInlineAdmin(nested_admin.NestedStackedInline):
    model = PaymentMethod
    extra = 0
    inlines = (PaymentMethodSettlementCycleInlineAdmin,)


class SettlementAccountInlineAdmin(nested_admin.NestedStackedInline):
    model = SettlementAccount
    extra = 0


class SettlementInformationInlineAdmin(nested_admin.NestedStackedInline):
    model = SettlementInformation
    extra = 0
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
