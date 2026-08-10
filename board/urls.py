from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('community/', views.PostListView.as_view(), name='community'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('<int:pk>/bookmark/', views.PostBookmarkView.as_view(), name='post_bookmark'),
    path('<int:post_pk>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
