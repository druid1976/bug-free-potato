from django.urls import path
from .views import QuestionAPIView, QuestionDetailAPIView, AnswerAPIView, CommentAPIView, VoteAPIView

urlpatterns = [
    path('questions/', QuestionAPIView.as_view(), name='questions'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question_detail'),
    path('questions/<int:question_id>/answers/', AnswerAPIView.as_view(), name='answers'),
    path('comments/<int:content_type_id>/<int:object_id>/', CommentAPIView.as_view(), name='comments'),
    path('votes/', VoteAPIView.as_view(), name='votes'),
]
