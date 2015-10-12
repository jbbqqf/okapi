from django.contrib import admin
from groups.models import Group, GroupForm, GroupUser, GroupUserForm, okaGroupForm, okaGroup

class okaGroupAdmin(admin.ModelAdmin):
    form = okaGroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent']

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent']

class GroupUserAdmin(admin.ModelAdmin):
    form = GroupUserForm
    list_display = ['user', 'group', 'role']
    search_fields = ['user', 'group', 'role']

admin.site.register(Group, GroupAdmin)
admin.site.register(okaGroup, okaGroupAdmin)
admin.site.register(GroupUser, GroupUserAdmin)
