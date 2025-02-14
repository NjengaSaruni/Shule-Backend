import pytest
from rest_framework.exceptions import ValidationError

from llm.serializers import OllamaPromptSerializer

def test_ollama_prompt_serializer_valid_data():
    valid_data = {
        "prompt": "test_prompt",
        "model": "test_model",
        "stream": False
    }
    serializer = OllamaPromptSerializer(data=valid_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_data

def test_ollama_prompt_serializer_default_model():
    data = {
        "prompt": "test_prompt",
        "stream": False
    }
    serializer = OllamaPromptSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["model"] == "deepseek-r1"

def test_ollama_prompt_serializer_default_stream():
    data = {
        "prompt": "test_prompt",
        "model": "test_model"
    }
    serializer = OllamaPromptSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["stream"] is False

def test_ollama_prompt_serializer_missing_prompt():
    data = {
        "model": "test_model",
        "stream": False
    }
    serializer = OllamaPromptSerializer(data=data)
    assert not serializer.is_valid()
    assert "prompt" in serializer.errors

def test_ollama_prompt_serializer_empty_prompt():
    data = {
        "prompt": "",
        "model": "test_model",
        "stream": False
    }
    serializer = OllamaPromptSerializer(data=data)
    assert not serializer.is_valid()
    assert "prompt" in serializer.errors