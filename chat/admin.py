from django.contrib import admin
from chat.models import Channel, ChannelForm, ChannelMember, ChannelMemberForm, ChannelGroup, ChannelGroupForm, Post, PostForm

class ChannelAdmin(admin.ModelAdmin):
    form = ChannelForm
    list_display = ['name', 'public', 'active', 'created',]
    search_fields = ['name',]

class ChannelMemberAdmin(admin.ModelAdmin):
    form = ChannelMemberForm
    list_display = ['channel', 'user', 'permissions',]
    search_fields = ['channel', 'user', 'permissions',]

class ChannelGroupAdmin(admin.ModelAdmin):
    form = ChannelGroupForm
    list_display = ['channel', 'group', 'permissions',]
    search_fields = ['channel', 'group', 'permissions',]

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['channel', 'date', 'author', 'type', 'content']
    search_fields = ['channel', 'author', 'content']

admin.site.register(Channel, ChannelAdmin)
admin.site.register(ChannelMember, ChannelMemberAdmin)
admin.site.register(ChannelGroup, ChannelGroupAdmin)
admin.site.register(Post, PostAdmin)
