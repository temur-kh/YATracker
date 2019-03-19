from django.db import models
from user_manager.models import (
    Student,
    Instructor,
)

from django.contrib.auth import get_user_model
User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    students = models.ManyToManyField(Student, related_name='projects')
    instructor = models.ForeignKey(
        Instructor,
        related_name='projects',
        on_delete=models.SET_NULL,
        null=True,
    )

