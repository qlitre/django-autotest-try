from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('post_detail/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post_create/', views.PostCreate.as_view(), name='post_create'),
    path('post_update/<int:pk>/', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', views.PostDelete.as_view(), name='post_delete')
]
