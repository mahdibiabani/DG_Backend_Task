from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'completed', 'due_date', 'created_at', 'modified_at')
    list_filter = ('completed', 'due_date', 'created_at', 'user')  
    search_fields = ('title', 'description')  
    ordering = ('-created_at',)  
