from django import forms
from .models import Article


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]


class NewArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]
