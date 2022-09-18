from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Post


class LoggedInTestCase(TestCase):
    """各テストクラスで共通の事前準備処理をオーバーライド"""

    def setUp(self) -> None:
        """テストメソッド実行前の事前設定"""
        # テスト用アカウントの作成
        self.password = 'password123'
        self.test_user = get_user_model().objects.create_user(
            username='test_user',
            email='testuser@email.com',
            password=self.password
        )
        # テスト用アカウントをログインさせる
        self.client.login(username=self.test_user.username, email=self.test_user.email, password=self.password)


class TestPostCreate(LoggedInTestCase):
    """PostCreateのテスト"""

    def test_create_post_success(self):
        """記事作成の成功をテスト"""
        # 記事データを作成
        params = {'title': 'テストタイトル',
                  'text': '本文'}
        response = self.client.post(reverse_lazy('blog:post_create'), params)
        # 一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('blog:post_list'))
        # データベースへ登録されたことを検証
        self.assertEqual(Post.objects.filter(title='テストタイトル').count(), 1)

    def test_create_post_failure(self):
        """記事作成の失敗をテスト"""
        # データを空で作成した場合の失敗を検証
        response = self.client.post(reverse_lazy('blog:post_create'))
        self.assertFormError(response, form='form', field='title', errors='このフィールドは必須です。')

        # タイトルのみ入れた場合の失敗を検証
        params = {'title': 'タイトル'}
        response = self.client.post(reverse_lazy('blog:post_create'), params)
        self.assertFormError(response, form='form', field='text', errors='このフィールドは必須です。')

        # 本文のみ入れて作成した場合の失敗を検証
        params = {'text': '本文'}
        response = self.client.post(reverse_lazy('blog:post_create'), params)
        self.assertFormError(response, form='form', field='title', errors='このフィールドは必須です。')

        # ログアウトしている場合
        self.client.logout()
        params = {'title': 'ログアウトユーザー',
                  'text': '本文\n本文'}
        response = self.client.post(reverse_lazy('blog:post_create'), params)
        # ログインページへのリダイレクトを検証
        self.assertRedirects(response, '/login/?next=/post_create/')
        # データが追加されていないことを検証
        self.assertEqual(Post.objects.filter(title='ログアウトユーザー').count(), 0)


class TestPostUpdate(LoggedInTestCase):
    """PostUpdateのテスト"""

    def test_update_post_success(self):
        """記事編集の成功をテスト"""
        # テスト用データの作成
        post = Post.objects.create(title='編集前', text='本文')
        # 編集処理を実行
        params = {'title': '編集後', 'text': '編集後の本文'}
        response = self.client.post(reverse_lazy('blog:post_update', kwargs={'pk': post.pk}), params)

        # 詳細ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('blog:post_detail', kwargs={'pk': post.pk}))

        # データが編集されたことを検証
        post_updated = Post.objects.get(pk=post.pk)
        self.assertEqual(post_updated.title, "編集後")
        self.assertEqual(post_updated.text, "編集後の本文")

    def test_update_post_failure(self):
        """編集処理の失敗をテスト"""
        # 存在しないデータの編集が失敗することを検証
        response = self.client.post(reverse_lazy('blog:post_update', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

        # ログアウトしている場合
        post = Post.objects.create(title='編集前', text='本文')
        self.client.logout()
        params = {'title': '編集後', 'text': '編集後の本文'}
        response = self.client.post(reverse_lazy('blog:post_update', kwargs={'pk': post.pk}), params)
        # ログインページへのリダイレクトを検証
        self.assertRedirects(response, f'/login/?next=/post_update/{post.pk}/')
        # データが編集されていないことの検証
        self.assertEqual(Post.objects.get(pk=post.pk).title, '編集前')


class TestPostDelete(LoggedInTestCase):
    """PostDeleteのテスト"""

    def test_delete_post_success(self):
        """削除処理の成功をテスト"""
        # テスト用データの作成
        post = Post.objects.create(title='タイトル', text='本文')

        # 削除処理を実行
        response = self.client.post(reverse_lazy('blog:post_delete', kwargs={'pk': post.pk}))

        # 一覧ページへのリダイレクトを検証
        self.assertRedirects(response, reverse_lazy('blog:post_list'))

        # 削除されたことを検証
        self.assertEqual(Post.objects.filter(pk=post.pk).count(), 0)

    def test_delete_post_failure(self):
        """削除処理の失敗をテスト"""
        # 存在しないデータの削除が失敗することを検証
        response = self.client.post(reverse_lazy('blog:post_delete', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

        # ログアウトしている場合
        post = Post.objects.create(title='タイトル', text='本文')
        self.client.logout()
        response = self.client.post(reverse_lazy('blog:post_delete', kwargs={'pk': post.pk}))
        # ログインページへのリダイレクトを検証
        self.assertRedirects(response, f'/login/?next=/post_delete/{post.pk}/')
        # データが削除されていないことを検証
        self.assertEqual(Post.objects.filter(pk=post.pk).count(), 1)
