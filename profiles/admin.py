from django.contrib import admin
from profiles.models import Profile, ProfileForm

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ['nick', 'birthday', 'note', 'gender', 'user']
    search_fields = ['nick', 'birthday', 'note']

admin.site.register(Profile, ProfileAdmin)
