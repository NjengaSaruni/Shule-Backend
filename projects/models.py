from django.db import models
from core.models import AbstractBase
from users.models import AbstractCreatorBase, User

class Project(AbstractCreatorBase):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
