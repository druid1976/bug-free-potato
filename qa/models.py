# bu ne be: from tkinter.constants import CHORD
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import CustomUser


# Create your models here.


class Question(models.Model):
    STATUS = ((0, "OPEN"),
              (1, "CLOSED")
              )

    question = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='written_questions_by_student')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = models.ManyToManyField("Tags", blank=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    image = models.ImageField(upload_to='questions/', null=True, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.question} | {self.author}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"Answer by {self.author} to {self.question}"


class Comment(models.Model):
    object_id = models.PositiveIntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Comment by {self.author}"


class Tags(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Vote(models.Model):
    VOTE_CHOICES = (
        (0, 'None'),
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    vote = models.IntegerField(choices=VOTE_CHOICES, default=0)

    class Meta:
        unique_together = [('user', 'question'), ('user', 'answer'), ('user', 'comment')]
