from django.contrib import admin
from users.models import User, UserForm, Profile, ProfileForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['login', 'profile', 'locked']
    search_fields = ['login', 'profile']

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ['firstname', 'lastname', 'surname', 'birthday', 'gender']
    search_fields = ['firstname', 'lastname', 'surname', 'birthday', 'note', 'gender']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
