from django.db import models
from django.db.models import IntegerField
from accounts.models import CustomUser
# Create your models here.


class Question(models.Model):
    STATUS = ((1, "OPEN"),
              (2, "CLOSED")
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

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.question} | {self.author}"


class CustomText(models.Model):
    ATOM = ((0, "Answer"),
            (1, "Comment")
            )

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers_for_question')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='texts_by_student')
    type = IntegerField(choices=ATOM, default=0)
    text = models.TextField()
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)


class Tags(models.Model):
    tag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag

