from rest_framework import serializers

class OllamaPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    model = serializers.CharField(default="llama3")  # Optional: let users choose the model
    stream = serializers.BooleanField(default=False) 