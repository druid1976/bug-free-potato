from django.urls import path
from .views import *


urlpatterns = [

    path('question/create/', QuestionCreateView.as_view(), name='create_quest'),
    path('questions/', QuestionAllView.as_view(), name='all_questions'),
    path('myquestions/', MyQuestionAllView.as_view(), name='my_questions'),
    path('question/<int:question_id>/', QuestionDetailView.as_view(), name='detailed_question'),
    path('question/<int:question_id>/vote/', QuestionVoteView.as_view(), name='question_vote'),
    path('question/<int:question_id>/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path("question/<int:question_id>/delete/", QuestionDeleteView.as_view(), name="delete_question"),
    path('json_pull_request/', QuestionNamesViaJson.as_view(), name='json_pull_request'),
]
