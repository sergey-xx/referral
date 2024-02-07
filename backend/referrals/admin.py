from django.contrib import admin

from .models import RefCodes, Invited


@admin.register(RefCodes)
class RefCodesAdmin(admin.ModelAdmin):
    pass


@admin.register(Invited)
class InvitedAdmin(admin.ModelAdmin):
    pass
