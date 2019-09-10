from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'parent_category_id']


admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'nickname', 'text']


admin.site.register(Comment, CommentAdmin)

