from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import CustomLoginForm
from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.


class LoginView(View):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the user details page with the student's number
                return redirect(reverse('blank', kwargs={'student_number': user.student_number}))
        return render(request, self.template_name, {'form': form})


class SignUpView(View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # logger
            return redirect(reverse('user_details.html'))
        return render(request, self.template_name, {'form': form})


class UserDetailsView(LoginRequiredMixin, View):
    template_name = 'accounts/user_details.html'
    login_url = 'login'

    def get(self, request, student_number):
        if request.user.student_number == student_number:
            user = get_object_or_404(CustomUser, student_number=student_number)
            return render(request, self.template_name, {'user': user})
        else:
            return redirect('login')


class UserUpdateView(LoginRequiredMixin, View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_update.html'
    login_url = 'login'

    def get(self, request, student_number):
        if request.user.student_number == student_number:
            user = get_object_or_404(CustomUser, student_number=student_number)
            return render(request, self.template_name, {'user': user})


class BlankView(LoginRequiredMixin, View):
    template_name = 'accounts/blank.html'
    login_url = 'login'

    def get(self, request):
        context = {
            'section_links': [
                {'name': 'Profile', 'url': 'user_details', 'param': request.user.student_number},
                {'name': 'Courses', 'url': 'courses', 'param': request.user.student_number},
            ]
        }
        return render(request, self.template_name, context)


class CoursesView(LoginRequiredMixin, View):
    template_name = 'accounts/courses.html'
    login_url = 'login'
    courses = CustomUser.objects.

    def get(self, request, student_number):
        context = {}
