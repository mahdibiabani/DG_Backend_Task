from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.utils.timezone import now
from django_filters import rest_framework as filters

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .filters import TaskFilter
from .models import Task
from .serializers import TaskSerializer



class TaskViewSet(viewsets.ModelViewSet):
    """
    managing all tasks

    Admins can:
    - View all tasks.
    - Manage all tasks.

    Regular users can:
    - View, create, update, and delete only their own tasks.
    - Cannot delete completed tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_class = TaskFilter 
    search_fields = ['title', 'description']
    http_method_names = ['get', 'post','put', 'delete', 'head']

    def get_queryset(self):
        """
        Return all tasks for admin users and only the user's own tasks for regular users.
        """
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all tasks",
        operation_description="List all tasks for admin users and only the user's own tasks for regular users.",
        responses={200: TaskSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all tasks for admin users and only the user's own tasks for regular users.
        """
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="Retrieve a task by ID",
        operation_description="Retrieve a task by ID. Admins can retrieve any task, regular users can only retrieve their own tasks.",
        responses={200: TaskSerializer, 404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a task by ID. Admins can retrieve any task, regular users can only retrieve their own tasks.
        """
        return super().retrieve(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="Create a new task",
        operation_description="Create a new task. The due date cannot be in the past.",
        request_body=TaskSerializer,
        responses={201: TaskSerializer, 400: 'The due date cannot be in the past.'}
    )


    def create(self, request, *args, **kwargs):
        """
        Create a new task. The due date cannot be in the past.
        """
        due_date = request.data.get("due_date")
        if due_date and due_date < now().date().isoformat():
            return Response(
                {"detail": "The due date cannot be in the past."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the task
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary="Update an existing task",
        operation_description="Update an existing task. The due date cannot be in the past.",
        request_body=TaskSerializer,
        responses={200: TaskSerializer, 400: 'The due date cannot be in the past.'}
    )

    def update(self, request, *args, **kwargs):
        """
        Update an existing task. The due date cannot be in the past.
        """
        due_date = request.data.get("due_date")
        if due_date and due_date < now().date().isoformat():
            return Response(
                {"detail": "The due date cannot be in the past."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().update(request, *args, **kwargs)



    @swagger_auto_schema(
        operation_summary="Delete task by id",
        operation_description="Delete a task. Regular users cannot delete completed tasks.",
        responses={204: 'No Content', 400: 'You cannot delete a completed task.'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a task. Regular users cannot delete completed tasks.
        """
        task = self.get_object()
        if not request.user.is_staff and task.completed:
            return Response(
                {"detail": "You cannot delete a completed task."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

