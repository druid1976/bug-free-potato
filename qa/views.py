from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from .models import *
# Create your views here.


class QuestionViewer(View):
    template_name = 'qa/all_questions.html'

    def get(self, request):
        questions = Question.objects.all()

        pager = Paginator(questions, 5)
        page_number = request.GET.get('page', 1)
        questions = pager.page(page_number)

        context = {'questions': questions}
        return render(request, self.template_name, context)


class QuestionDetailedViewer(View):
    template_name = 'qa/detailed_question.html'

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        tags = question.tags.all()
        context = {'question': question,
                   'tags': tags}
        return render(request, self.template_name, context)


class MyQuestionViewer(LoginRequiredMixin, View):
    template_name = 'qa/all_my_question.html'
    login_url = 'accounts:login'

    def get(self, request):
        questions = Question.objects.filter(author__student_number=request.user.student_number)

        pager = Paginator(questions, 5)
        page_number = request.GET.get('page', 1)
        questions = pager.page(page_number)

        context = {'questions': questions}
        return render(request, self.template_name, context)


class MyCommentsViewer(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'qa/all_my_comments.html'

    def get(self, request):
        comments = CustomText.objects.filter(type=1, author__student_number=request.user.student_number)
        questions = [comment.question for comment in comments]
        pager = Paginator(comments, 10)
        page_number = request.GET.get('page', 1)
        comments = pager.page(page_number)

        context = {'comments': comments,
                   'questions': questions}
        return render(request, self.template_name, context)
