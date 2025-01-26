from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
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
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        # Admins can see all tasks; regular users see only their tasks
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


    def create(self, request, *args, **kwargs):
       

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
        if "user" in request.data and not request.user.is_staff:
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

        return super().update(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        # Prevent deletion of completed tasks
        task = self.get_object()
        if not request.user.is_staff and task.completed:
            return Response(
                {"detail": "You cannot delete a completed task."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

