from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Address


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'full_name', 'city', 'is_default', 'created_at']
    list_filter = ['is_default', 'city', 'created_at']
    search_fields = ['user__username', 'full_name', 'title', 'city']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
