from django.db import models
from accounts.models import CustomUser
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
    instructor = models.OneToOneField('accounts.CustomUser', on_delete=models.SET_NULL,
                                      blank=True, null=True, related_name='course_instructor')

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
    day = models.IntegerField(choices=DAYS, default=0)
    starting_hour = models.TimeField(blank=True, null=True)
    ending_hour = models.TimeField(blank=True, null=True)
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
    # year is for non-informant semesters for creation of curriculum
    year = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}, ({self.start_date} - {self.end_date})"

# Can be made as a new app?


class Curriculum(models.Model):
    program_name = models.CharField(max_length=200)
    program_code = models.CharField(max_length=100)
    semester = models.ManyToManyField("Semester", related_name='curricula')
    courses = models.ManyToManyField(Course, related_name='curricula')

    def __str__(self):
        return f"{self.program_name}"


class AcademicDream(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_academic_dream', null=True)
    courses = models.ForeignKey(Course, related_name='user_in_course',
                                on_delete=models.SET_NULL, blank=True, null=True)
    grade = models.IntegerField(default=-1, blank=True)
    section = models.ForeignKey(Section, related_name='section_academic_dream',
                                on_delete=models.SET_NULL, blank=True, null=True)
    curriculum = models.ForeignKey("Curriculum", related_name='curry_academic_dream',
                                   on_delete=models.CASCADE, blank=True, null=True)

    def calculate_grade(self):
        total_note = 0
        total_credits = 0
        ad = self.objects.exclude(grade=-1)
        for arcade in ad:
            if arcade.courses and arcade.courses.max_credit_points.isdigit():
                creditty = int(arcade.courses.max_credit_points)
                total_note += creditty * arcade.grade / 100
                total_credits += creditty
        return total_note / total_credits
