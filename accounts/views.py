from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from courses.views import AcademicDream
from .forms import *
from .models import CustomUser

# Create your views here.

# can be made into app !?


class BlankView(LoginRequiredMixin, View):
    template_name = 'accounts/blank.html'
    login_url = 'accounts:login'

    def get(self, request):

        context = {
            'section_links': [
                {'name': 'Profile',
                 'url': reverse('accounts:user_details', kwargs={'student_number': request.user.student_number})},
                {'name': 'My Courses',
                 'url': reverse('courses:path_finder')},
                {'name': 'Semester List',
                 'url': reverse('courses:semester_list')},
                {'name': 'My Curriculum',
                 'url': reverse('courses:courses_curriculum', kwargs={'program_code': request.user.study})},
                {'name': 'QBank',
                 'url': reverse('qa:all_questions')},
                {'name': 'dexter',
                 'url': reverse('courses:dexter')},
            ]
        }
        return render(request, self.template_name, context)


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
                return redirect(reverse('accounts:blank'))
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
            return redirect(reverse('accounts:user_details'))
        return render(request, self.template_name, {'form': form})


class UserDetailsView(LoginRequiredMixin, View):
    template_name = 'accounts/user_details.html'
    login_url = 'accounts:login'

    def get(self, request, student_number):
        if request.user.student_number == student_number:
            user = get_object_or_404(CustomUser, student_number=student_number)
            return render(request, self.template_name, {'user': user})
        else:
            return redirect(reverse('accounts:login'))


class UserUpdateView(LoginRequiredMixin, View):
    form_class = CustomUserUpdateForm
    template_name = 'accounts/user_update.html'
    login_url = 'accounts:login'

    def get(self, request, student_number):
        if request.user.student_number == student_number:
            user = get_object_or_404(CustomUser, student_number=student_number)
            form = self.form_class(instance=user)
            return render(request, self.template_name, {'form': form, 'user': user})
        else:
            return redirect(reverse('accounts:login'))

    def post(self, request, student_number):
        if request.user.student_number == student_number:
            user = get_object_or_404(CustomUser, student_number=student_number)
            form = self.form_class(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:blank'))
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('accounts:login')

'''

class CoursesView(LoginRequiredMixin, View):
    template_name = 'accounts/my_courses.html'
    login_url = 'accounts:login'

    def get(self, request, student_number):
        if request.user.student_number == student_number and not None:
            user = get_object_or_404(CustomUser, student_number=student_number)
            dreams = AcademicDream.objects.filter(student=user)
            pear = [dreams.courses for dreams in dreams]
            context = {'courses': pear,
                       'url': reverse('accounts:my_courses', kwargs={'student_number': request.user.student_number})}
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('accounts:login'))



        pager = Paginator(questions, 5)
        page_number = request.GET.get('page', 1)
        questions = pager.page(page_number)
'''