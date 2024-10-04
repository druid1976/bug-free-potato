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
    login_url = 'accounts:login'

    def get(self, request, *args, **kwargs):
        s = Semester.objects.all()
        return render(request, self.template_name, {'semesters': s[2:]})


class CourseDetailView(LoginRequiredMixin, View):
    template_name = 'courses/course_detail.html'

    def get(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)
        curr = CurriculumCourseSemester.objects.get(course=course)
        try:
            acad = curr.semcor_academic_dream.get(student=request.user)
        except AcademicDream.DoesNotExist:
            acad = AcademicDream.objects.create(student=request.user, curriculum_course_semester=curr, grade=-1)

        # Group sections via numeros pre-sectionpacket era
        sections_by_number = {}
        for section in course.sections.all():
            if section.section_number not in sections_by_number:
                sections_by_number[section.section_number] = []
            sections_by_number[section.section_number].append(section)

        context = {
            'course': course,
            'sections_by_number': sections_by_number,
            'grade': acad.grade,
            'current_status': self.get_status_from_grade(acad.grade)
        }
        return render(request, self.template_name, context)

    def get_status_from_grade(self, grade):
        if grade == -1:
            return "not_taken"
        elif grade == 101:
            return "now_taking"
        elif grade >= 50:
            return "passed"
        else:
            return "failed"

    def post(self, request, course_code):
        course = get_object_or_404(Course, course_code=course_code)
        curr = CurriculumCourseSemester.objects.get(course=course)
        acad, created = AcademicDream.objects.get_or_create(student=request.user, curriculum_course_semester=curr)

        data = json.loads(request.body)
        status = data.get('status_change')
        grade = data.get('grade')

        if status == 'not_taken':
            grade = -1
        elif status == 'now_taking':
            grade = 101
        elif status in ['passed', 'failed']:
            if grade is None:
                return JsonResponse({'error': 'Grade must be provided.'}, status=400)

            try:
                grade = int(grade)
                if grade < 0 or grade > 100:
                    return JsonResponse({'error': 'Invalid grade. Grade must be between 0 and 100.'}, status=400)
            except ValueError:
                return JsonResponse({'error': 'Grade must be a valid number.'}, status=400)

        acad.grade = grade
        acad.save()

        return JsonResponse({
            'status': status,
            'grade': grade,
        })


class CurriculumView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'courses/curriculum.html'

    def get(self, request, program_code):
        student = request.user
        currs = CurriculumCourseSemester.objects.filter(program_code=student.study)

        backtobackwtf = []
        for cur in currs:
            academic_dreams = cur.semcor_academic_dream.filter(student=student)
            status = 'not_taken'  # Default status

            if academic_dreams.exists():
                academic_dream = academic_dreams.first()
                if academic_dream.grade == -1:
                    status = 'not_taken'
                elif academic_dream.grade == 101:
                    status = 'now_taking'
                elif 50 <= academic_dream.grade <= 100:
                    status = 'passed'
                else:
                    status = 'failed'
            backtobackwtf.append({'curr': cur, 'status': status})

        context = {
            'courses_status': backtobackwtf,
            'program_code': program_code
        }
        return render(request, self.template_name, context)






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
        student = request.user
        curr = CurriculumCourseSemester.objects.filter(program_code =student.study)
        suggested_courses = []
        for cur in curr:
            if cur.semester.semester_id - 2 == student.semester_of_student:
                suggested_courses.append(cur.course)
           # if cur.semester.semester_id - 2 < student.semester_of_student :


        context = {
            'suggested_courses': suggested_courses,
        }
        return render(request, 'courses/dexter.html', context=context)
