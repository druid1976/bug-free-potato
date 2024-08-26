from django.db import models
from rooms.models import Rooms
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    credit_points = models.IntegerField()
    credit_hours = models.IntegerField()
    instructor = models.ForeignKey("accounts.Instructor", on_delete=models.CASCADE)
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_number = models.CharField(max_length=10)
    schedule = models.CharField(max_length=100)
    classroom = models.ForeignKey("Rooms", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.course.title} Section {self.section_number}"

class Semester(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name}, ({self.start_date} - {self.end_date} )"
