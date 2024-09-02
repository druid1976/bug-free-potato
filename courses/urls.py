from django.urls import path
from courses.views import SemesterListView
from accounts import views

app_name = 'courses'
urlpatterns = [
    path('semester/', SemesterListView.as_view(), name='semester_list'),

]





