from django.urls import path
from accounts.views import *

app_name = 'accounts'

urlpatterns = [path('login/', LoginView.as_view(), name='login'),
               path('signup/', SignUpView.as_view(), name='signup'),
               path('user/<str:student_number>/', UserDetailsView.as_view(), name='user_details'),
               path('user/<str:student_number>/edit', UserUpdateView.as_view(), name='user_update'),
               path('', BlankView.as_view(), name='blank'),
               path('user/<str:student_number>/my_courses', CoursesView.as_view(), name='my_courses'),
               ]
