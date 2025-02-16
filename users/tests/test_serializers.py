import pytest
from rest_framework.exceptions import ValidationError
from users.serializers import UserSerializer, UserCreateSerializer, AbstractCreatorUserSerializerMixin
from users.models import User
from unittest.mock import patch

@pytest.mark.django_db
def test_user_serializer():
    user = User.objects.create(
        email='test@example.com', 
        first_name='Test',
        last_name='User')
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['email'] == 'test@example.com'
    assert data['first_name'] == 'Test'
    assert data['last_name'] == 'User'
    assert 'is_staff' in data
    assert 'is_active' in data

@pytest.mark.django_db
def test_user_create_serializer():
    data = {
        'email': 'create@example.com',
        'password': 'password123',
        'first_name': 'Create',
        'last_name': 'User'
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == 'create@example.com'
    assert user.check_password('password123')
    assert user.first_name == 'Create'
    assert user.last_name == 'User'

@pytest.mark.django_db
@patch('users.middleware.get_current_user')
def test_abstract_creator_user_serializer_mixin_create(mock_get_current_user):
    mock_get_current_user.return_value = User.objects.create(
        email='creator@example.com')
    data = {
        'email': 'mixincreate@example.com',
        'password': 'password123',
        'first_name': 'MixinCreate',
        'last_name': 'User'
    }
    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == 'mixincreate@example.com'