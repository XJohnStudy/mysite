from django.contrib import admin
from .models import ReadNum, ReadDetail

@admin.register(ReadNum)
class ReadNum(admin.ModelAdmin):
  list_display = ('content_object', 'read_num')

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
  list_display = ('date', 'content_object', 'read_num')