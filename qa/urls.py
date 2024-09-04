from django.urls import path

from qa.views import *

urlpatterns = [

    path('qbank', QuestionViewer.as_view(), name='all_questions'),
    path('my_questions', MyQuestionViewer.as_view(), name='my_questions'),
    path('<int:question_id>/details', QuestionDetailedViewer.as_view(), name='question_detail'),
]
