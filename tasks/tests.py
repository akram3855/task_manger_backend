from django.test import TestCase

# Create your tests here.
# tasks/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Set up a test API key in the headers for all requests
        self.client.defaults['HTTP_X_API_KEY'] = 'test-api-key'

        # Create some test tasks
        self.task1 = Task.objects.create(title='Task A', priority='high', status='todo', due_date='2023-01-01T10:00:00Z')
        self.task2 = Task.objects.create(title='Task B', priority='low', status='in_progress', due_date='2023-01-02T10:00:00Z')
        self.task3 = Task.objects.create(title='Task C', priority='medium', status='done', due_date='2023-01-03T10:00:00Z')
        self.task4 = Task.objects.create(title='Task D', priority='medium', status='todo', due_date='2023-01-04T10:00:00Z')

    def test_list_tasks(self):
        """
        Test listing all tasks and ensure pagination works.
        """
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

    def test_create_task(self):
        """
        Test creating a new task.
        """
        data = {'title': 'New Task', 'status': 'todo', 'priority': 'low'}
        response = self.client.post(reverse('task-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 5)

    def test_retrieve_task(self):
        """
        Test retrieving a single task by ID.
        """
        response = self.client.get(reverse('task-detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task A')

    def test_update_task(self):
        """
        Test updating an existing task.
        """
        data = {'title': 'Updated Task A', 'status': 'done'}
        response = self.client.patch(reverse('task-detail', args=[self.task1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task A')
        self.assertEqual(self.task1.status, 'done')

    def test_delete_task(self):
        """
        Test deleting a task.
        """
        response = self.client.delete(reverse('task-detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 3)

    def test_filter_by_status_and_priority(self):
        """
        Test filtering tasks by status and priority.
        """
        response = self.client.get(reverse('task-list'), {'status': 'todo', 'priority': 'medium'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task D')

    def test_search_by_title(self):
        """
        Test searching tasks by title.
        """
        response = self.client.get(reverse('task-list'), {'search': 'Task B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task B')

    def test_sort_by_priority(self):
        """
        Test sorting tasks by priority (high to low).
        """
        response = self.client.get(reverse('task-list'), {'ordering': '-priority'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Task A')
        self.assertEqual(response.data['results'][1]['title'], 'Task C')
        self.assertEqual(response.data['results'][2]['title'], 'Task D')
        self.assertEqual(response.data['results'][3]['title'], 'Task B')
