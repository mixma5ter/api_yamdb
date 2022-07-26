from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role',)
    search_fields = ('username', 'first_name', 'last_name', 'email', )
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
