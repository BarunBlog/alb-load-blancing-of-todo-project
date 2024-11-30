from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})



class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer