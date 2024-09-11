# bu ne be: from tkinter.constants import CHORD
from PIL import Image
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

    image = models.ImageField(upload_to='qa/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image is not None:
            img = Image.open(self.image)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)


    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.question} | {self.author}"


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    answer = models.BooleanField(default=False)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    image = models.ImageField(upload_to='comments/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)
            if img.height > 400 or img.width > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f"Comment by {self.author}"


class Tags(models.Model):
    tag = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag


class Vote(models.Model):
    VOTE_CHOICES = (
        (0, 'none'),
        (1, 'up_votes'),
        (-1, 'down_votes'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes', null=True, blank=True)
    vote = models.IntegerField(choices=VOTE_CHOICES, default=0)

    class Meta:
        unique_together = [('user', 'question'), ('user', 'comment')]



