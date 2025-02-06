from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProjectListCreateView

urlpatterns = [
	path('', ProjectListCreateView.as_view(), name='project-list-create'),
]