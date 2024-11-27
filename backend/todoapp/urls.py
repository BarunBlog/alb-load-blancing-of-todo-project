from django.urls import path
from .views import TaskList, TaskDetail

urlpatterns = [
    path('task-list/', TaskList.as_view(), name='task-list'),
    path('task-detail/', TaskDetail.as_view(), name='task-detail'),
]