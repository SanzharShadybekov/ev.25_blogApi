from django.contrib.auth.models import User
from rest_framework import generics, permissions
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.filters import SearchFilter

from . import serializers


class CustomLoginView(LoginView):
    permission_classes = (permissions.AllowAny,)


class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'email')


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)





