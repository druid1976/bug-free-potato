from django.contrib import admin
from .models import Course, Section, Semester, AcademicDream, Curriculum

# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(AcademicDream)
admin.site.register(Curriculum)