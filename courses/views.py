from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import *

# Create your views here.

'''
class CourseView(LoginRequiredMixin, View):
    model = Course
    context_object_name = 'courses'
'''


class SemesterListView(LoginRequiredMixin, View):
    template_name = 'courses/semester_list.html'
    login_url = 'accounts:login'

    def get(self, request, *args, **kwargs):
        s = Semester.objects.all()
        return render(request, self.template_name, {'semesters': s[2:]})

