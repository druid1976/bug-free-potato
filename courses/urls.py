from django.urls import path
from courses.views import *

app_name = 'courses'

urlpatterns = [
    path('dex/', Dexter.as_view(), name='dexter'),
    path('search/', CourseSearchView.as_view(), name='course_search'),
    path('semester_list/', SemesterListView.as_view(), name='semester_list'),
    path('<str:course_code>/', CourseDetailView.as_view(), name='course_detail'),
    path('list/', CourseListView.as_view(), name='course_list'), # THIS IS FOR AFTER THE CREATION OF DEXTER
    path('curr/<str:program_code>/', CurriculumView.as_view(), name='courses_curriculum'),

]





