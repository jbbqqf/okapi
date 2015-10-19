from django.contrib import admin

from themes.models import UserInterface, UserInterfaceForm, Theme, ThemeForm, UserTheme, UserThemeForm

class UserInterfaceAdmin(admin.ModelAdmin):
    form = UserInterfaceForm
    list_display = ['name', 'comment',]
    search_fields = ['name', 'comment',]

class ThemeAdmin(admin.ModelAdmin):
    form = ThemeForm
    list_display = ['ui', 'name', 'comment',]
    search_fields = ['ui', 'name', 'comment',]

class UserThemeAdmin(admin.ModelAdmin):
    form = UserThemeForm
    list_display = ['user', 'theme',]
    search_fields = ['user', 'theme',]

admin.site.register(UserInterface, UserInterfaceAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(UserTheme, UserThemeAdmin)
