from .models import Post
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label


class PostCreateForm(forms.ModelForm):
    """記事作成フォーム"""

    class Meta:
        model = Post
        fields = ('title', 'text')
