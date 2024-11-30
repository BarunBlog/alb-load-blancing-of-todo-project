from django.urls import path
from .views import health_check, TaskList, TaskDetail

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('task-list/', TaskList.as_view(), name='task-list'),
    path('task-detail/', TaskDetail.as_view(), name='task-detail'),
]