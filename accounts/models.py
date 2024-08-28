from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey, SET_NULL, IntegerField, OneToOneField
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
               (7, "7th"),
               (8, "8th"),
               (9, "9th"),
               )

    SUBJECT_CHOICES = (
        ("CS", "Computer Science"),
        ("ENG", "Engineering"),
        ("BIO", "Biology"),
    )

    student_number = models.BigIntegerField(unique=True, blank=True, null=True)
    status = models.IntegerField(choices=WHO, default=1)
    # is_student = models.BooleanField(default=True)
    year_of_student = models.IntegerField(choices=NUMBERS, default=1, null=True, blank=True)
    # daha sonra ilk kayıt olduğu anda yılını belirrtiği
    # vakit normal zaman diliminden semestrı belirtilebilir
    semester_of_student = IntegerField(default=1, null=True, blank=True)
    """"
    For some reason doesn't work!
     semester = ForeignKey("Semester", null=True, blank=True,
    related_name="enrolled_students", on_delete=models.CASCADE)
    """
    study = models.CharField(choices=SUBJECT_CHOICES, max_length=50, null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

# Can be made as a new app?


class AcademicDream(models.Model):
    student = OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='academic_dream', null=True)
    courses = models.ForeignKey(Course, related_name='user_in_course', on_delete=SET_NULL, blank=True, null=True)
    grade = models.IntegerField(null=True, blank=True)


""" 
According to status value courses = taker or giver
"""