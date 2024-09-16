from django.http import HttpResponseRedirect
from django.urls import path
from accounts.views import *

app_name = 'accounts'


urlpatterns = [
    path('mac/', BlankView.as_view(), name='blank'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:student_number>/', UserDetailsView.as_view(), name='user_details'),
    path('<str:student_number>/edit', UserUpdateView.as_view(), name='user_update'),
]