from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from accounts.models import User, OtpCode, Address, NewsLetter


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    search_fields = ('email', 'phone_number', 'full_name')

    fieldsets = (
        (None, {'fields':('email', 'phone_number', 'full_name', 'password')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('email', 'phone_number', 'full_name', 'password1', 'password2')}),
    )

    ordering = ('full_name',)
    filter_horizontal = ()


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'email', 'created')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'neighbourhood', 'street', 'alley', 'building')


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'created', 'status')


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)