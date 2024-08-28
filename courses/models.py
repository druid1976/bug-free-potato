from django.db import models
from django.db.models import IntegerField, TimeField

# from datetime import time --> this is for creating time(9,0)
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200)
    course_description = models.TextField()
    course_code = models.CharField(max_length=200)
    max_credit_points = models.CharField(max_length=10)
    is_it_offered = models.BooleanField(default=False)
    language = models.CharField(default="ENG", max_length=10)
    semester = models.ForeignKey("Semester",
                                 on_delete=models.CASCADE,
                                 related_name="courses_for_semester",
                                 null=True, blank=True)
    instructor = models.OneToOneField('CustomUser', on_delete=models.SET_NULL, blank=True, null=True, related_name='course_instructor')

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

    DAYS = ((1, "MONDAY"),
            (2, "TUESDAY"),
            (3, "WEDNESDAY"),
            (4, "THURSDAY"),
            (5, "FRIDAY"),
            )

    section_number = models.CharField(max_length=10)
    day = IntegerField(choices=DAYS, default=0)
    starting_hour = TimeField(blank=True, null=True)
    ending_hour = TimeField(blank=True, null=True)
    room_name = models.CharField(max_length=50)
    building_name = models.CharField(choices=NAMES, max_length=100)
    floor_name = models.CharField(max_length=50)
    course = models.ForeignKey("Course",
                               on_delete=models.CASCADE,
                               related_name="sections",
                               null=True, blank=True)

    def __str__(self):
        return (f"Section {self.section_number} of {self.course.title} "
                f"on {self.day} {self.starting_hour} between "
                f"{self.ending_hour}")


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # year is for non-informant semesters
    year = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, ({self.start_date} - {self.end_date})"
