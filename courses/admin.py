from django.contrib import admin
from .models import Course, Section, Semester
# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Semester)
