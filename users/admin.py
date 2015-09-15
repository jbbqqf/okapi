from django.contrib import admin
from users.models import User, UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['login', 'profile_id', 'locked']
    search_fields = ['login', 'profile_id']

admin.site.register(User, UserAdmin)
