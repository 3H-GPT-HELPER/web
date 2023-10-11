from django.contrib import admin

# Register your models here.

from .models import UserCategory
from . import models

# class UserAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Users,UserAdmin)

# @admin.register(models.Users)
# class CustomUserAdmin(admin.ModelAdmin):
#     pass

class UserKeywordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserCategory,UserKeywordsAdmin)

