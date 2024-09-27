from django import forms

from chatroom.models import File
from .models import Question, Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'content', 'tags', 'image']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sor!',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your question in detail',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
        }
        labels = {
            'question': 'Question Title',
            'content': 'Description',
            'tags': 'Tags (Optional)',
            'image': 'Attach Image (Opsiyonel)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your comment here...',
                'rows': 4,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            })
        }
        labels = {
            'content': 'Your Comment',
            'image': 'Attach Image to comment...',
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control-file',

            })
        }