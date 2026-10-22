from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from solo.admin import SingletonModelAdmin

from .models import AdminUser, User

admin.site.register(User, UserAdmin)
admin.site.register(AdminUser, SingletonModelAdmin)
