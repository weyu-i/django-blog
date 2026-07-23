from django import forms

from blog.models import BlogCategory


class PubBlogForm(forms.Form):
    title=forms.CharField(max_length=200,min_length=2)
    content=forms.CharField(min_length=2)
    category=forms.IntegerField()
    def __str__(self):
        return self.title