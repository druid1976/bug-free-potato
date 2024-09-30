from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
from django.db.models import F
import json
# Create your views here.


from django.urls import reverse

#bunu arama fonksiyonun implemente edebilmek için eklemek zorunda kaldım no hate

class QuestionNamesViaJson(LoginRequiredMixin, View):
    def get(self, request):
        questions = Question.objects.all()
        questions_list = []

        for question in questions:
            #reverse ile url çekiyorum, js'te isme tıklandığında direkt sayfaya yönlendirsin diye
            question_url = reverse('qa:detailed_question', kwargs={'question_id': question.id})
            variable_name = question.author
            name = variable_name.username
            questions_list.append({"question": question.question, "id": question.id, "url": question_url, "author": name})
            #idyi belki bir işime yarar diye gönderiyorum (bence gerek olmayacak da)
        context = {"questions": questions_list}
        return JsonResponse(context)


class QuestionAllView(View):

    @staticmethod
    def get(request):
        # GOT EM ACCORDING TO VOTESTATION
        # AGGREGATE = 1 TIME ANNOTATE = QUERY SET
        questions = Question.objects.annotate(vote_score=F('up_votes') - F('down_votes')).order_by('-vote_score')
        paginator = Paginator(questions, 5)
        page_number = request.GET.get('page')
        questions = paginator.get_page(page_number)

        return render(request, 'qa/all_questions.html', {'questions': questions})


class MyQuestionAllView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        questions = Question.objects.annotate(vote_score=F('up_votes') - F('down_votes')).order_by('-vote_score')
        q = questions.filter(author=request.user)
        paginator = Paginator(q, 5)
        page_number = request.GET.get('page')

        q = paginator.get_page(page_number)

        return render(request, 'qa/myquestions.html', {'questions': q})


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

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)

        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image', None)
        if not content:
            return JsonResponse({'message': 'Content not provided'})

        comment = Comment(content=content, author=request.user, question=question)
        comment.save()
        return JsonResponse({'message': 'Comment created',
                             'comment': {
                                 'author': request.user.username,
                                 'content': content,
                                 'image': comment.image.url if image else None,
                                 'id': comment.id,
                             }})


class QuestionCreateView(LoginRequiredMixin, View):
    login_url = 'accounts:login'
    template_name = 'qa/create_quest.html'

    def get(self, request):
        form = QuestionForm()
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def post(request):

        if request.FILES:
            form = QuestionForm(request.POST, request.FILES)
        else:
            form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()  # saves tags separately
            return redirect('qa:detailed_question', question_id=question.id)

        return render(request, 'qa/create_quest.html', {'form': form})


class QuestionDeleteView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    @staticmethod
    def post(request, question_id):
        try:
            question = get_object_or_404(Question, id=question_id, author=request.user)
            question.delete()
            return JsonResponse({'message': 'Question deleted'})
        except Question.DoesNotExist:
            return JsonResponse({'message': 'Question not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class CommentDeleteView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    @staticmethod
    def post(request, question_id, comment_id):
        comment = get_object_or_404(Comment,
                                    question_id=question_id,
                                    id=comment_id,
                                    author=request.user)
        if request.user != comment.author:
            return HttpResponseForbidden('You are not authorized to delete this comment')
        else:
            try:
                comment.delete()
                return JsonResponse({'message': 'Comment deleted'})
            except Comment.DoesNotExist:
                return JsonResponse({'message': 'Comment not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)


class QuestionVoteView(View):
    def post(self, request, question_id):
        try:
            question = get_object_or_404(Question, id=question_id)
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

            data = json.loads(request.body.decode('utf-8'))
            vote_type = data.get('vote_type')

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