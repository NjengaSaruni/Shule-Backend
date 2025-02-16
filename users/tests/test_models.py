import pytest
from django.contrib.auth import get_user_model

UserModel = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = UserModel.objects.create_user(
        email='test@example.com', 
        password='password123', 
        first_name='Test', 
        last_name='User')
    assert user.email == 'test@example.com'
    assert user.check_password('password123')
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError):
        UserModel.objects.create_user(email='', password='password123')

@pytest.mark.django_db
def test_create_superuser():
    superuser = UserModel.objects.create_superuser(
        email='admin@example.com', 
        password='admin123',
        first_name='Admin', 
        last_name='User')
    assert superuser.email == 'admin@example.com'
    assert superuser.check_password('admin123')
    assert superuser.first_name == 'Admin'
    assert superuser.last_name == 'User'
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser

@pytest.mark.django_db
def test_user_str():
    user = UserModel.objects.create_user(email='test@example.com', password='password123', first_name='Test', last_name='User')
    assert str(user) == 'test@example.com'