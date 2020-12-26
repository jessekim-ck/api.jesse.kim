from django.contrib import admin
from .models import Post, Category, Comment, DayLog
from django.contrib.auth.models import User
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin


# class PostAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'created', 'updated', 'is_private']


# admin.site.register(Post, PostAdmin)


class PostResource(resources.ModelResource):
    class Meta:
        model = Post
        fields = ('id', 'title', 'created', 'updated', 'text', 'category_id', 'writer_id', 'is_private')


class PostAdmin(ImportExportModelAdmin):
    resource_class = PostResource
    list_display = ['id', 'title', 'created', 'updated', 'is_private']


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
