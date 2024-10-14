from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
import json
from .models import *
import logging

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
        # Fetch all courses and prefetch related section packets and sections in one query
        courses = Course.objects.prefetch_related(
           # Prefetch('sectionpacket_set', queryset=SectionPacket.objects.prefetch_related('section'))
        )

        course_data = []
        for course in courses:
            packet_list = []
            for packet in course.sectionpacket_set.all():
                sections = packet.section.values('section_number', 'day', 'starting_hour',
                                                 'room_name', 'building_name', 'floor_name')
                packet_list.append({
                    'packet_id': packet.id,
                    'sections': list(sections)
                })

            course_data.append({
                'title': course.title,
                'course_code': course.course_code,
                'section_packets': packet_list
            })
        
        return JsonResponse({'course_data': course_data})


class Dexter(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        student = request.user
        curr = CurriculumCourseSemester.objects.filter(program_code=student.study)
        suggested_courses = []
        old_courses = []
        for cur in curr:
            if cur.semester.semester_id - 2 == student.semester_of_student:
                try:
                    academic_dream = cur.semcor_academic_dream.get(student=student)
                    if academic_dream.grade <= 50:
                        suggested_courses.append(cur.course)
                except AcademicDream.DoesNotExist:
                    academic_dream = AcademicDream.objects.create(student=request.user, curriculum_course_semester=cur,
                                                                  grade=-1)
                    suggested_courses.append(cur.course)

            if cur.semester.semester_id - 2 < student.semester_of_student:
                try:
                    academic_dream = cur.semcor_academic_dream.get(student=student)
                    if academic_dream.grade <= 50:
                        old_courses.append(cur.course)
                except AcademicDream.DoesNotExist:
                    academic_dream = AcademicDream.objects.create(student=request.user, curriculum_course_semester=cur,
                                                                  grade=-1)
                    old_courses.append(cur.course)

        context = {
            'suggested_courses': suggested_courses,
            'old_courses': old_courses
        }
        return render(request, 'courses/dexter.html', context=context)


class AcademicDreamSubmitView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def post(self, request):
        print("Request received")  # Debug statement
        try:
            data = json.loads(request.body)  # Parse the JSON body
            print("Data received:", data)  # Log the incoming data

            for entry in data:
                course_code = entry['course_code']
                section_packet_id = entry['section_packet_id']  # Use the correct key
                grade = entry['grade']

                # Fetch the course and curriculum semester
                course = Course.objects.get(course_code=course_code)
                curriculum_course_semester = CurriculumCourseSemester.objects.filter(course=course).first()

                # Fetch the SectionPacket instance
                section_packet = SectionPacket.objects.filter(id=section_packet_id).first()

                if curriculum_course_semester and section_packet:
                    # Update or create AcademicDream instance
                    academic_dream, created = AcademicDream.objects.update_or_create(
                        student=request.user,
                        curriculum_course_semester=curriculum_course_semester,
                        defaults={
                            'grade': grade,
                            'section_packet': section_packet,
                        }
                    )
                    if created:
                        print("Created new AcademicDream instance:", academic_dream)
                    else:
                        print("Updated existing AcademicDream instance:", academic_dream)
                else:
                    return JsonResponse({"success": False, "message": "Invalid course or section packet."}, status=400)

            return JsonResponse({"success": True, "message": "Academic Dream(s) processed successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
