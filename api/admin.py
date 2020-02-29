from django.contrib import admin
from .models import Post, Category, Comment, DayLog
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated', 'private']


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'parent_category_id']


admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'nickname', 'text']


admin.site.register(Comment, CommentAdmin)


class DayLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'condition', 'achievement', 'memo']


admin.site.register(DayLog, DayLogAdmin)
