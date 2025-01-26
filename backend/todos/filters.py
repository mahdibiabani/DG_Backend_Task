import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # Filter by due_date (exact match)
    due_date = django_filters.DateFilter(field_name="due_date", lookup_expr='exact', label="Due Date")
    
    # Filter by created_at (exact match)
    created_at = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='exact', label="Created At")
    
    
    class Meta:
        model = Task
        fields = ['due_date', 'created_at']
