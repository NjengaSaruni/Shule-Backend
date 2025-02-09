from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from llm.serializers import OllamaPromptSerializer

class OllamaAPIView(APIView):
    def post(self, request):
        serializer = OllamaPromptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        ollama_url = "http://localhost:11434/api/generate"
        
        try:
            # Send request to Ollama
            response = requests.post(
                ollama_url,
                json={
                    "model": data["model"],
                    "prompt": data["prompt"],
                    "stream": data["stream"]
                },
                stream=data["stream"]
            )
            response.raise_for_status()
            
            if data["stream"]:
                # Handle streaming response
                def generate_stream():
                    for line in response.iter_lines():
                        if line:
                            yield line.decode("utf-8") + "\n"
                return Response(generate_stream(), content_type="text/event-stream")
            else:
                # Handle non-streaming response
                return Response(response.json(), status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Ollama request failed: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )