from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
import json
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


class CourseDetailView(LoginRequiredMixin, View):
    template_name = 'courses/course_detail.html'

    def get(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)

        # Group sections via numero
        sections_by_number = {}
        for section in course.sections.all():
            if section.section_number not in sections_by_number:
                sections_by_number[section.section_number] = []
            sections_by_number[section.section_number].append(section)

        context = {
            'course': course,
            'sections_by_number': sections_by_number,
        }
        return render(request, self.template_name, context)


class CourseListView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'courses/course_list.html'

    def get(self, request):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})


class CurriculumView(LoginRequiredMixin, View):
    template_name = 'courses/curriculum.html'
    login_url = 'accounts:login'

    def get(self, request, program_code):
        if request.user is not None:
            student = request.user
            curr = Curriculum.objects.get(program_code=student.study)
            courses = curr.courses.all().order_by('semester__semester_id')

            ACDC = AcademicDream.objects.filter(courses__in=courses, student=student)
            ACDC_dict = {ad.courses.id: ad.grade for ad in ACDC}

            courses_status = []
            for course in courses:
                if course.id in ACDC_dict:
                    grade = ACDC_dict[course.id]
                    if grade >= 50:
                        status = 'passed'
                    elif grade == -1:
                        status = 'not_taken'
                    else:
                        status = 'failed'
                else:
                    status = 'not_taken'
                courses_status.append({
                    'course': course,
                    'status': status
                })
            context = {
                'courses_status': courses_status,
                'program_code': program_code
            }
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('accounts:login'))


class CourseSearchView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        courses = Course.objects.all()
        course_data = []

        for course in courses:
            section_query = Section.objects.filter(course=course)
            section_list = list(section_query.values('section_number', 'day', 'starting_hour',
                                                     'room_name', 'building_name', 'floor_name'))
            course_data.append({
                'title': course.title,
                'sections': section_list
            })
        context = {'course_data': course_data}
        return JsonResponse(context)


class Dexter(LoginRequiredMixin, View):

    login_url = 'accounts:login'

    def get(self, request):
        return render(request, 'courses/dexter.html')
