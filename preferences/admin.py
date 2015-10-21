from django.contrib import admin

from preferences.models import UserInterface, UserInterfaceForm, UserPref, UserPrefForm

class UserInterfaceAdmin(admin.ModelAdmin):
    form = UserInterfaceForm
    list_display = ['name', 'comment',]
    search_fields = ['name', 'comment',]

class UserPrefAdmin(admin.ModelAdmin):
    form = UserPrefForm
    list_display = ['user', 'ui', 'conf',]
    search_fields = ['user', 'ui', 'conf',]

admin.site.register(UserInterface, UserInterfaceAdmin)
admin.site.register(UserPref, UserPrefAdmin)
