from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course


# Create your models here.

class Student(AbstractUser):
    student_id = models.IntegerField(unique=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)

class Instructor(AbstractUser):
