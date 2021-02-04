from django.contrib import admin

from owners.models import Owner, PayGoComputationalManager


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    pass


@admin.register(PayGoComputationalManager)
class PayGoComputationalManagerAdmin(admin.ModelAdmin):
    pass
