import pytest
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
import requests
from ..views import OllamaAPIView

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def valid_payload():
    return {
        "model": "test_model",
        "prompt": "test_prompt",
        "stream": False
    }

@pytest.fixture
def invalid_payload():
    return {
        "model": "",
        "prompt": "test_prompt",
        "stream": False
    }

@pytest.mark.django_db
def test_ollama_api_view_post_valid_payload(api_client, valid_payload):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"result": "success"}

        response = api_client.post('/llm/ollama/', valid_payload, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"result": "success"}

@pytest.mark.django_db
def test_ollama_api_view_post_invalid_payload(api_client, invalid_payload):
    response = api_client.post('/llm/ollama/', invalid_payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_ollama_api_view_post_request_exception(api_client, valid_payload):
    with patch('requests.post', side_effect=requests.exceptions.RequestException):
        response = api_client.post('/llm/ollama/', valid_payload, format='json')

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "Ollama request failed" in response.json()["error"]