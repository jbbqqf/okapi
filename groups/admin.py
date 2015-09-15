from django.contrib import admin
from groups.models import Group, GroupForm

class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    list_display = ['name', 'url', 'ml', 'description']
    search_fields = ['name', 'url', 'ml', 'description']

admin.site.register(Group, GroupAdmin)
