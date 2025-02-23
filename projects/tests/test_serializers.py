import pytest
from rest_framework.test import APIClient
from projects.models import Project
from projects.serializers import ProjectSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def project_data(user):
    return {
        'name': 'Test Project',
        'description': 'Test Description',
        'created_by': user,
        'updated_by': user
    }

@pytest.fixture
def project(project_data):
    return Project.objects.create(**project_data)

@pytest.fixture
def serializer(project):
    return ProjectSerializer(instance=project)

@pytest.mark.django_db
def test_contains_expected_fields(serializer):
    data = serializer.data
    expected_fields = {'id', 'name', 'description', 'created_at', 'updated_at', 'created_by', 'updated_by', 'start_date', 'end_date'}
    assert set(data.keys()) == expected_fields

@pytest.mark.django_db
def test_name_field_content(serializer, project_data):
    data = serializer.data
    assert data['name'] == project_data['name']

@pytest.mark.django_db
def test_description_field_content(serializer, project_data):
    data = serializer.data
    assert data['description'] == project_data['description']

@pytest.mark.django_db
def test_serializer_validation(user):
    invalid_data = {
        'name': '',  # Empty name should be invalid
        'description': 'Test Description',
        'created_by': user.pk,
        'updated_by': user.pk
    }
    serializer = ProjectSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors
