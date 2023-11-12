from django.contrib import admin
from post.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    search_fields = ['title', 'user__username']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    search_fields = ['text', 'user__username']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
