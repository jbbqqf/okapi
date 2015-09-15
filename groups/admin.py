from django.contrib import admin
from groups.models import Group, GroupForm

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ['id', 'name', 'url', 'mailing', 'description', 'parent_id']
    search_fields = ['name', 'url', 'mailing', 'description', 'parent_id']

admin.site.register(Group, GroupAdmin)
