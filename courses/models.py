from django.db import models
from django.conf import settings
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200)
    course_description = models.TextField()
    course_code = models.CharField(max_length=200)
    max_credit_points = models.CharField(max_length=10)
    students_credit_point = models.IntegerField(blank=True, null=True)
    offered_semester = models.ForeignKey("Semester", on_delete=models.CASCADE)
    language = models.CharField(default="ENG", max_length=10)
    section = models.ForeignKey("Section", on_delete=models.CASCADE, related_name="courses")
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE, related_name="courses_for_semester")

    def __str__(self):
        return self.title


class Section(models.Model):

    NAMES = (("ENG", "FACULTY OF ENGINEERING"),
             ("LAW", "FACULTY OF LAW"),
             ("MED", "FACULTY OF MEDICINE"),
             ("LANG", "FACULTY OF LANGUAGE"),
             ("LIT", "FACULTY OF LITERATURE"),
             ("SCI", "FACULTY OF SCIENCE"),
             )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    section_number = models.CharField(max_length=10)
    schedule = models.CharField(max_length=100)
    room_name = models.CharField(max_length=50)
    building_name = models.CharField(choices=NAMES, max_length=100)
    floor_name = models.CharField(max_length=50)

    def __str__(self):
        return f"Section {self.section_number} of {self.course.title}"


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name}, ({self.start_date} - {self.end_date})"
