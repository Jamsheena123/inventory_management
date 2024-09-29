# from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item

class ItemTests(APITestCase):
    def test_create_item(self):
        response = self.client.post('/api/items/', {'name': 'Test Item', 'description': 'Test Description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description')
        response = self.client.get(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description')
        response = self.client.put(f'/api/items/{item.id}/', {'name': 'Updated Item', 'description': 'Updated Description'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item(self):
        item = Item.objects.create(name='Test Item', description='Test Description')
        response = self.client.delete(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
