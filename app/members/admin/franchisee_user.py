from django.contrib import admin

from members.models import FranchiseeUser


class FranchiseeUserAdmin(admin.ModelAdmin):
    fields = ('email',)


admin.site.register(FranchiseeUser, FranchiseeUserAdmin)
