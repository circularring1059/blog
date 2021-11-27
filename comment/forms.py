from django import forms
from .models import MultipyComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = MultipyComment
        fields = ["body"]
