from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
# Create your views here.


class QuestionCreateView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'qa/create_quest.html'

    def get(self, request):
        form = QuestionForm()
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def post(request):
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()  # saves tags separately
            return redirect('qa:detailed_question', question_id=question.id)
        return render(request, 'qa/create_quest.html', {'form': form})


class QuestionVoteView(View):
    def post(self, request, question_id):
        try:
            question = get_object_or_404(Question, id=question_id)
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            vote_type = request.POST.get('vote_type')

            vote, created = Vote.objects.get_or_create(user=user, question=question)

            if vote_type == 'upvote':
                if vote.vote != 1:
                    question.up_votes += 1
                    if vote.vote == -1:
                        question.down_votes -= 1
                    vote.vote = 1
            elif vote_type == 'downvote':
                if vote.vote != -1:
                    question.down_votes += 1
                    if vote.vote == 1:
                        question.up_votes -= 1
                    vote.vote = -1

            vote.save()
            question.save()

            return JsonResponse({
                'up_votes': question.up_votes,
                'down_votes': question.down_votes
            })

        except FileNotFoundError as e:
            print(f"File not found: {str(e)}")
            return JsonResponse({'error': 'File not found, missing image'}, status=404)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


class QuestionAllView(View):

    @staticmethod
    def get(request):
        questions = Question.objects.all()
        paginator = Paginator(questions, 10)
        page_number = request.GET.get('page')
        questions = paginator.get_page(page_number)

        return render(request, 'qa/all_questions.html', {'questions': questions})


class QuestionDetailView(View):
    @staticmethod
    def get(request, question_id):

        question = get_object_or_404(Question, id=question_id)
        comments = Comment.objects.filter(question=question)  # comment getter of q
        comment_form = CommentForm()

        return render(request, 'qa/detailed_question.html', {
            'question': question,
            'comments': comments,
            'comment_form': comment_form,
        })

    @staticmethod
    def post(request, question_id):
        question = get_object_or_404(Question, id=question_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question  # Linker of the comment to the question
            comment.save()
            return redirect('qa:detailed_question', question_id=question.id)

        comments = Comment.objects.filter(question=question)

        return render(request, 'qa/detailed_question.html', {
            'question': question,
            'comments': comments,
            'comment_form': form,
        })


class CommentDeleteView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    @staticmethod
    def get(request, question_id, comment_id):
        try:
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment.delete()
            return JsonResponse({'message': 'Comment deleted'})
        except Comment.DoesNotExist:
            return JsonResponse({'message': 'Comment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        