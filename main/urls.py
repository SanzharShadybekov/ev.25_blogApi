from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.PostListCreateView.as_view()),
    path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
]
