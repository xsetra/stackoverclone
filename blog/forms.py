from django import forms
from .models import Post, Comment, CommentOfComment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('baslik', 'yazi')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class CommentOfCommentForm(forms.ModelForm):

    class Meta:
        model = CommentOfComment
        fields = ('text', )
