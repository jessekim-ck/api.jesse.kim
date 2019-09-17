from django.contrib import admin
from .models import Post, Category, Comment
from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created', 'updated']


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'parent_category_id']


admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'nickname', 'text']


admin.site.register(Comment, CommentAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'date_joined', 'last_login']


admin.site.register(User, UserAdmin)

