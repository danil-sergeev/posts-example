from django.contrib import admin
from users.models import User
# Register your models here.


class CustomUserAdminView(admin.ModelAdmin):
    pass


admin.site.register(User, CustomUserAdminView)
