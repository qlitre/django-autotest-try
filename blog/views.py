from django.views import generic
from .models import Post
from django.urls import reverse_lazy
from .forms import LoginForm, PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'blog/login.html'
    success_url = reverse_lazy('blog:post_list')


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'blog/logout.html'


class PostList(generic.ListView):
    """記事一覧ページ"""
    template_name = 'blog/post_list.html'
    model = Post
    ordering = '-updated_at'


class PostDetail(generic.DetailView):
    """記事詳細ページ"""
    template_name = 'blog/post_detail.html'
    model = Post


class PostCreate(LoginRequiredMixin, generic.CreateView):
    """記事作成ページ"""
    template_name = 'blog/post_create.html'
    model = Post
    success_url = reverse_lazy('blog:post_list')
    form_class = PostCreateForm


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    """記事編集ページ"""
    template_name = 'blog/post_create.html'
    model = Post
    form_class = PostCreateForm

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    """記事削除ページ"""
    template_name = 'blog/post_delete.html'
    model = Post
    success_url = reverse_lazy('blog:post_list')
