from django.contrib import admin

from members.models import FranchiseeUser, PayGoUser, AgencyUser


@admin.register(FranchiseeUser)
class FranchiseeUserAdmin(admin.ModelAdmin):
    pass


@admin.register(AgencyUser)
class AgencyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(PayGoUser)
class PayGoUserAdmin(admin.ModelAdmin):
    pass
