from django.contrib import admin
import django.contrib.auth.admin
from django.utils.translation import ugettext_lazy as _
from . import models


class ArticleAdmin(admin.ModelAdmin):
   list_display = (
        'title', 'is_private', 'date_created', 'date_updated', 'uid', 'pk')
   readonly_fields = ('uid', 'date_created', 'date_updated')
   search_fields = 'title',


class CategoryAdmin(admin.ModelAdmin):
   list_display = (
        'display_name', 'date_created', 'date_updated', 'uid', 'pk')
   search_fields = 'display_name',


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    fieldsets = (
        (None, {'fields': (
            'uid', 'username', 'password', 'first_ip_addr', 'last_ip_addr'
        )}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'is_verified_email', 'timezone'
        )}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions'
        )}),
        (_('Important dates'), {'fields': (
            'date_joined', 'date_updated', 'expiration_date', 'last_login',
            'last_seen',
        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'timezone')}
        ),
    )
    list_display = (
        '__str__', 'is_staff', 'is_active', 'is_expired',
        'is_verified_email', 'email', 'get_timezone_display',
        'date_joined', 'date_updated', 'last_seen', 'last_ip_addr', 'uid')
    list_display_links = ('uid', '__str__')
    list_filter = ('is_verified_email', 'is_staff', 'is_active')
    readonly_fields = (
        'uid', 'date_updated', 'last_login', 'last_seen',
        'first_ip_addr', 'last_ip_addr')


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.User, UserAdmin)
