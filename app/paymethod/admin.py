from django.contrib import admin

from paymethod.models import PaymentMethod, PaymentMethodSettlementCycle, SettlementInformation, SettlementAccount


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethodSettlementCycle)
class PaymentMethodSettlementCycleAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementInformation)
class SettlementInformationAdmin(admin.ModelAdmin):
    pass


@admin.register(SettlementAccount)
class SettlementAccountAdmin(admin.ModelAdmin):
    pass
