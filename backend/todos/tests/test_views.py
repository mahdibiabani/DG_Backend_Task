from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta
from todos.models import Task

User = get_user_model()


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta
from todos.models import Task

User = get_user_model()


class TaskViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword', email='adminuser@example.com')
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            due_date=date.today() + timedelta(days=1),
            completed=False
        )
        self.url = reverse('task-list')  

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'due_date': (date.today() + timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')

    def test_create_task_with_past_due_date(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Task',
            'description': 'New task description',
            'due_date': (date.today() - timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('The due date cannot be in the past.', response.data['detail'])

    def test_update_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task',
            'due_date': (date.today() + timedelta(days=2)).isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_update_task_change_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        data = {
            'title': 'Updated Task',
            'user': self.admin_user.id,
            'due_date': (date.today() + timedelta(days=2)).isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You cannot change the user field.', response.data['detail'])

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_completed_task(self):
        self.client.force_authenticate(user=self.user)
        self.task.completed = True
        self.task.save()
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You cannot delete a completed task.', response.data['detail'])

    def test_admin_can_see_all_tasks(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.count())

    def test_user_can_see_only_own_tasks(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.filter(user=self.user).count())


