from django.contrib import admin
from groups.models import Group, GroupForm, GroupUser, GroupUserForm

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent_id']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent_id']

class GroupUserAdmin(admin.ModelAdmin):
    form = GroupUserForm
    list_display = ['user', 'group', 'role']
    search_fields = ['user', 'group', 'role']

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupUser, GroupUserAdmin)
