from django.contrib import admin

from enroll.models import user_involved

@admin.register(user_involved)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'Room_ka_name']
