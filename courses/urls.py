from django.urls import path
from courses.views import *
from accounts import views

app_name = 'courses'
urlpatterns = [
    path('semester/', SemesterListView.as_view(), name='semester_list'),
    path('<str:course_code>', CourseDetailView.as_view(), name='course_detail'),
    path('', CourseListView.as_view(), name='course_list'),
    path('curr/<str:program_code>', CurriculumView.as_view(), name='courses_curriculum'),

]





