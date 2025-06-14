from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Admin-zone user
    """
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'role', 'admin')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email',)
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)