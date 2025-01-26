from django.test import TestCase
from django.contrib.auth import get_user_model
from todos.models import Task
from datetime import date

User = get_user_model()


class TaskModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a task for testing
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            due_date=date.today(),
            completed=False
        )

    def test_task_creation(self):
        # Test if the task is created correctly
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task.')
        self.assertEqual(self.task.due_date, date.today())
        self.assertFalse(self.task.completed)
        self.assertEqual(self.task.user, self.user)

    def test_task_str_method(self):
        # Test the __str__ method of the Task model
        self.assertEqual(str(self.task), 'Test Task')

    def test_task_default_values(self):
        # Test the default values of the Task model
        self.assertFalse(self.task.completed)

    def test_task_update(self):
        # Test updating a task
        self.task.title = 'Updated Task'
        self.task.completed = True
        self.task.save()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertTrue(self.task.completed)

    def test_task_delete(self):
        # Test deleting a task
        task_id = self.task.id
        self.task.delete()
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)

