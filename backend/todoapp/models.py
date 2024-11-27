from django.db import models
from django.core.exceptions import ValidationError


class Task(models.Model):
    """
    Represents a single to-do task.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    # Fields for the Task model
    title = models.CharField(max_length=200, help_text="Short description of the task.")
    description = models.TextField(blank=True, null=True, help_text="Detailed information about the task.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', help_text="Current status of the task.")
    priority = models.IntegerField(default=1, help_text="Priority level of the task, where 1 is the highest priority.")
    due_date = models.DateField(blank=True, null=True, help_text="Deadline for completing the task.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the task was last updated.")

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.priority < 1 or self.priority > 5:
            raise ValidationError("Priority must be between 1 (highest) and 5 (lowest).")
