from rest_framework import serializers

class OllamaPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True)
    model = serializers.CharField(default="deepseek-r1")  # Optional: let users choose the model
    stream = serializers.BooleanField(default=False) 