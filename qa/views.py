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
            return redirect('detailed_question', question_id=question.id)
        return render(request, 'qa/create_quest.html', {'form': form})


class QuestionVoteView(View):
    @staticmethod
    def post(request, question_id):
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
        comment = get_object_or_404(Comment, id=comment_id, question_id=question_id)

        if comment.author != request.user:
            return HttpResponseForbidden("Yalnız kardeşim onu sen silemezsin")
        comment.delete()
        return JsonResponse({'message': 'Comment deleted succeessfullly!'})


'''
class QuestionAPIView(APIView):

    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerAPIView(APIView):

    def get(self, request, question_id):
        try:
            answers = Answer.objects.filter(question_id=question_id)
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request, question_id):
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['question'] = question.id
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentAPIView(APIView):

    def get(self, request, content_type_id, object_id):
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
            comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
        except ContentType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, content_type_id, object_id):
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
        except ContentType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data['content_type'] = content_type.id
        data['object_id'] = object_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteAPIView(APIView):

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_vote = Vote.objects.get(
                    user=request.user,
                    content_type_id=request.data['content_type'],
                    object_id=request.data['object_id']
                )
                existing_vote.vote = request.data['vote']
                existing_vote.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Vote.DoesNotExist:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''