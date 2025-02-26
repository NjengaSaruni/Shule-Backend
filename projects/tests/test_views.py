import pytest
from django.urls import reverse
from projects.models import Project
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='testuser@gmail.com', 
        password='testpassword')

@pytest.fixture
def token(user):
    return Token.objects.create(user=user)

@pytest.fixture
def project1(user):
    return Project.objects.create(
        name='Project 1', 
        description='Description 1',
        created_by=user)

@pytest.fixture
def project2(user):
    return Project.objects.create(
        name='Project 2', 
        description='Description 2', 
        created_by=user)

@pytest.fixture
def project_list_url():
    return reverse('project-list-create')

@pytest.fixture
def project_detail_url(project1):
    return reverse('project-retrieve-update-destroy', args=[project1.pk])

@pytest.mark.django_db
class TestProjectViews:
    def test_project_list_GET(self, api_client, user, token, project1, project2, project_list_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(project_list_url)

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_project_create_POST(self, api_client, user, token, project_list_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'name': 'New Project',
            'description': 'New Description',
        }
        response = api_client.post(project_list_url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Project.objects.count() == 1 
        
        assert Project.objects.get(title='New Project').description == 'New Description'

    def test_project_detail_GET(self, api_client, user, token, project1, project_detail_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(project_detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Project 1'

    def test_project_update_PUT(self, api_client, user, token, project1, project_detail_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'title': 'Updated Project',
            'description': 'Updated Description',
        }
        response = api_client.put(project_detail_url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Project.objects.get(pk=project1.pk).title == 'Updated Project'

    def test_project_delete_DELETE(self, api_client, user, token, project1, project_detail_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(project_detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Project.objects.count() == 0

    def test_project_list_unauthenticated(self, api_client, project_list_url):
        response = api_client.get(project_list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_create_POST_unauthenticated(self, api_client, project_list_url):
        data = {
            'title': 'New Project',
            'description': 'New Description',
        }
        response = api_client.post(project_list_url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Project.objects.count() == 0

    def test_project_detail_GET_unauthenticated(self, api_client, project1, project_detail_url):
        response = api_client.get(project_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_update_PUT_unauthenticated(self, api_client, project1, project_detail_url):
        data = {
            'title': 'Updated Project',
            'description': 'Updated Description',
        }
        response = api_client.put(project_detail_url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Project.objects.get(pk=project1.pk).title == 'Project 1'

    def test_project_delete_DELETE_unauthenticated(self, api_client, project1, project_detail_url):
        response = api_client.delete(project_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Project.objects.count() == 1

    def test_project_create_POST_invalid_data(self, api_client, user, token, project_list_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'description': 'New Description', # Missing title
        }
        response = api_client.post(project_list_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Project.objects.count() == 0

    def test_project_update_PUT_invalid_data(self, api_client, user, token, project1, project_detail_url):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'title': '', # Invalid title
            'description': 'Updated Description',
        }
        response = api_client.put(project_detail_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Project.objects.get(pk=project1.pk).title == 'Project 1'

    def test_project_detail_not_found(self, api_client, user, token):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('project-detail', args=[999])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_project_delete_not_found(self, api_client, user, token):
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = reverse('project-detail', args=[999])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Project.objects.count() == 0