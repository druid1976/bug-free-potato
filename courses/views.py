from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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


class CourseDetailView(View):
    template_name = 'courses/course_detail.html'

    def get(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)
        return render(request, self.template_name, {'course': course})


class CourseListView(View):
    template_name = 'courses/course_list.html'

    def get(self, request):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})


class CurriculumView(LoginRequiredMixin, View):
    template_name = 'courses/curriculum.html'
    login_url = 'accounts:login'

    def get(self, request, program_code):
        if request.user.study == "CENG" and not None:
            curr = Curriculum.objects.get(program_code=program_code)
            courses = curr.courses.all()
            context = {'courses': courses, 'program_code': program_code}
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('accounts:login'))

