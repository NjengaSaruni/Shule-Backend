from django.urls import path
from .views import OllamaAPIView

urlpatterns = [
    path('ollama/', OllamaAPIView.as_view(), name='ollama-api'),
]