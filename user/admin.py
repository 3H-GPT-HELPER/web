from django.contrib import admin

# Register your models here.

from .models import User,UserKeywords

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User,UserAdmin)

class UserKeywordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserKeywords,UserKeywordsAdmin)

