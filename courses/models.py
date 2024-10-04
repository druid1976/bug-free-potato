from email._header_value_parser import Section

from django.db import models
from accounts.models import CustomUser
# from datetime import time --> this is for creating time(9,0)
# Create your models here.

#auth model
class Course(models.Model):
    title = models.CharField(max_length=200)
    course_description = models.TextField()
    course_code = models.CharField(max_length=200)
    max_credit_points = models.CharField(max_length=10)
    language = models.CharField(default="ENG", max_length=10)
    # Buradaki genel semester bilgisi
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

#silinecekti ama kaldı

class SectionPacket(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,)
    section = models.ManyToManyField(Section)

    def __str__(self):
        sections = ", ".join([str(s.section_number) for s in self.section.all()])
        return f"{self.course.title}, Sections: {sections}"


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


#keep track of the
class CurriculumCourseSemester(models.Model):
    program_name = models.CharField(max_length=200, default="Computer science")
    program_code = models.CharField(max_length=100, default="CENG")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.program_name} ({self.program_code}) - {self.course.title} for {self.semester.name}"



class GivenCoursesAndTheSemestersOfThem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="given_courses")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="given_courses")


class AcademicDream(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_academic_dream')
    curriculum_course_semester = models.ForeignKey(CurriculumCourseSemester, on_delete=models.CASCADE,
                                                   related_name="semcor_academic_dream")
    grade = models.IntegerField(default=-1, blank=True)
    section_packet = models.ForeignKey(SectionPacket, related_name='section_academic_dream',
                                       on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        course_info = f"{self.curriculum_course_semester}"
        section_info = f", Section: {self.section_packet}" if self.section_packet else ""
        grade_info = f", Grade: {self.grade}" if self.grade != -1 else ", Grade: N/A"
        return f"{self.student.get_full_name()} - {course_info}{section_info}{grade_info}"

    def status(self):
        grade_info = f", Grade: {self.grade}" if self.grade != -1 else ", Grade: N/A"
        return grade_info

    # program_code gelecek buraya kayıt sırasında

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
