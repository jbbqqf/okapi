from django.contrib import admin
from chat.models import Post, PostForm

class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['date', 'author', 'type', 'content']
    search_fields = ['author', 'content']

admin.site.register(Post, PostAdmin)
