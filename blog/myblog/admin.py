from django.contrib import admin
from .models import Post, Category, Comment



class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

    list_display_links = ("id", "title")
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category")

    list_display_links = ("id", "title", "user", "category")
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "content", "created_at")

    list_display_links = ("id", "post", "user", "content", "created_at")
admin.site.register(Comment, CommentAdmin)
