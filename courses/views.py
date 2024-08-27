from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import *
# Create your views here.


class CourseView(LoginRequiredMixin, View):
    model = Course
    context_object_name = 'courses'
