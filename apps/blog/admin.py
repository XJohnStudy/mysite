from django.contrib import admin
from .models import BlogType, Blog
# , ReadNum

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
  list_display = ('id', 'type_name')
  ordering = ('id',)

@admin.register(Blog)
class Blog(admin.ModelAdmin):
  list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')
  ordering = ('id',)

# @admin.register(ReadNum)
# class ReadNum(admin.ModelAdmin):
#   list_display = ('blog', 'read_num')