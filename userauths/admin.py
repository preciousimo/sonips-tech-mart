from django.contrib import admin
from userauths.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
admin.site.register(User, UserAdmin)