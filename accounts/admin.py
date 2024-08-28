from django.contrib import admin
from .models import CustomUser, AcademicDream

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AcademicDream)