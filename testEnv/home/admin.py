from django.contrib import admin
from .models import Blog , Category, Post



class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Blog, BlogAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
 
    list_display_links = ('id', 'title')
 
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category')
 
    list_display_links = ('id', 'title', 'user', 'category')
 
admin.site.register(Post, PostAdmin)