import socket
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})



class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)  # Get the default response
        hostname = socket.gethostname()  # Get the backend server identifier
        response.data["backend_server"] = hostname  # Add the backend identifier to the response
        return response


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer