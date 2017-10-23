from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Key, Profile, Site, User


class KeyInline(admin.TabularInline):
    model = Key
    extra = 1


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('avatar', 'note')}),
    )
    inlines = (
        KeyInline,
        ProfileInline,
    )


admin.site.register(Site)
admin.site.register(User, UserAdmin)
