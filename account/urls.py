from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),  # accounts/
    path('<int:pk>/', views.UserDetailView.as_view()),  # accounts/<id>/
    path('login/', views.CustomLoginView.as_view()),
    path('logout/', views.CustomLogoutView.as_view()),
    path('register/', views.UserRegisterView.as_view()),  # accounts/register/
]
