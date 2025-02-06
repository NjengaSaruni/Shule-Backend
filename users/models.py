from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from core.models import AbstractBase
from shule_backend import settings
from users.middleware import get_current_user

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBase, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class AbstractCreatorBase(AbstractBase):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_created',
        null=True,
        on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_updated',
        null=True,
        on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        
        if not self.pk:
            self.created_by = current_user
        self.modified_by = current_user
        
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True 