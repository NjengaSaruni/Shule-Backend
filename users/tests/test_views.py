import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return User.objects.create_user(email='testuser@gmail.com', password='testpass')

@pytest.mark.django_db
def test_user_create_view(api_client):
    url = reverse('user-create')
    data = {
        'email': 'testuser@gmail.com',
        'password': 'newpass',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email='testuser@gmail.com').exists()

@pytest.mark.django_db
def test_user_list_view(api_client, create_user):
    url = reverse('user-list')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['email'] == 'testuser@gmail.com'