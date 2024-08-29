from django.urls import path
from accounts.views import LoginView, SignUpView, UserDetailsView, UserUpdateView, BlankView, CourseView

urlpatterns = [path('login/', LoginView.as_view(), name='login'),
               path('signup/', SignUpView.as_view(), name='signup'),
               path('user/<str:student_number>/', UserDetailsView.as_view(), name='user_details'),
               path('user/<str:student_number>/edit',UserUpdateView.as_view(), name='user_update'),
               path('', BlankView.as_view(), name='blank'),
               path('user/<str:student_number>/courses', CourseView.as_view(), name='courses'),
               ]
