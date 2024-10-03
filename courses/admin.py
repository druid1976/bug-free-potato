from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(AcademicDream)
admin.site.register(CurriculumCourseSemester)
admin.site.register(SectionPacket)