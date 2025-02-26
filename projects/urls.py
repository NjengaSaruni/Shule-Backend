from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView

urlpatterns = [
	path('', ProjectListCreateView.as_view(), name='project-list-create'),
	path('<pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),
]