from django import forms
from .models import AcademicDream, Course, Section


class AcademicDreamForm(forms.ModelForm):
    class Meta:
        model = AcademicDream
        fields = ['courses', 'section']  # userdan aldığım tek inputlar

    # addan queryseti çekip yerleşiyor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['courses'].queryset = Course.objects.all()
        self.fields['section'].queryset = Section.objects.all()

