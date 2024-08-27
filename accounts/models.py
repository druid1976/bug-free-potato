from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import Course

# Create your models here.

"""
An abstract base class implementing a fully featured User model with
admin-compliant permissions.

Username and password are required. Other fields are optional.
username
first_name
last_name
email
"""


class CustomUser(AbstractUser):

    WHO = ((1, "STUDENT"),
           (2, "INSTRUCTOR")
           )

    NUMBERS = ((1, "1st"),
               (2, "2nd"),
               (3, "3rd"),
               (4, "4th"),
               (5, "5th"),
               (6, "6th"),
               )

    SUBJECT_CHOICES = (
        ("CS", "Computer Science"),
        ("ENG", "Engineering"),
        ("BIO", "Biology"),
    )

    user_id = models.IntegerField(unique=True)
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_in_course', null=True)
    status = models.IntegerField(choices=WHO, default="STUDENT")
    # is_student = models.BooleanField(default=True)
    year = models.IntegerField(choices=NUMBERS, default=1, null=True, blank=True)
    # for student
    study = models.CharField(choices=SUBJECT_CHOICES, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.get_full_name()


""" 
According to status value courses = taker or giver
"""