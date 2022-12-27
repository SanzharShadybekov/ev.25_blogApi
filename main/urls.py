from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.PostListCreateView.as_view()),
]
