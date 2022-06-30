


from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Posts,Comment

class NewPost(forms.ModelForm):
    class Meta:
        model=Posts
        fields=('image','caption',)

class UserComment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment',)