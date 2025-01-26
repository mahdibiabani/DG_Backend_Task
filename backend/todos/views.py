from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for authenticated users to manage their tasks with enhanced validations.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only access their own tasks
        return Task.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Check if the user already has a task (enforce one-to-one relationship)
        if Task.objects.filter(user=request.user).exists():
            return Response(
                {"detail": "You can only create one task at a time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Perform additional validations for `due_date`
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

    def update(self, request, *args, **kwargs):
        # Prevent the user from changing the user field
        if "user" in request.data:
            return Response(
                {"detail": "You cannot change the user field."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate `due_date` if present
        due_date = request.data.get("due_date")
        if due_date and due_date < now().date().isoformat():
            return Response(
                {"detail": "The due date cannot be in the past."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Proceed with updating the task
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Prevent deletion of completed tasks
        task = self.get_object()
        if task.completed:
            return Response(
                {"detail": "You cannot delete a completed task."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

