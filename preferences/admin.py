from django.contrib import admin

from preferences.models import UserInterface, UserInterfaceForm, UserTheme, UserThemeForm

class UserInterfaceAdmin(admin.ModelAdmin):
    form = UserInterfaceForm
    list_display = ['name', 'comment',]
    search_fields = ['name', 'comment',]

class UserThemeAdmin(admin.ModelAdmin):
    form = UserThemeForm
    list_display = ['user',]
    search_fields = ['user',]

admin.site.register(UserInterface, UserInterfaceAdmin)
admin.site.register(UserTheme, UserThemeAdmin)
