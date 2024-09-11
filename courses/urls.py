from django.urls import path
from courses.views import *

app_name = 'courses'

urlpatterns = [
    path('dex/', Dexter.as_view(), name='dexter'),
    path('search/', CourseSearchView.as_view(), name='course_search'),
    path('courses/<int:course_id>/sections/', CourseSectionsView.as_view(), name='course_sections'),
    path('semester_list/', SemesterListView.as_view(), name='semester_list'),
    path('<str:course_code>/', CourseDetailView.as_view(), name='course_detail'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('curr/<str:program_code>/', CurriculumView.as_view(), name='courses_curriculum'),

]





