from django.contrib.auth.models import User
from rest_framework import generics, permissions, mixins
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import serializers
from .models import Follow


class CustomModelViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    pass


class CustomLoginView(LoginView):
    permission_classes = (permissions.AllowAny,)


class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer


class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'email')

    def get_permissions(self):
        if self.action in ('retrieve', 'follow', 'unfollow'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.UserDetailSerializer
        return serializers.UserListSerializer

    @action(['POST'], detail=True)
    def follow(self, request, pk):
        following_user = self.get_object()
        user = request.user
        if following_user == user:
            return Response('You cannot follow yourself!', status=400)
        if user.followers.filter(following=following_user).exists():
            return Response('You already followed!', status=400)
        Follow.objects.create(follower=user, following=following_user)
        return Response('Successfully followed!', status=201)

    # .../api/v1/accounts/id/unfollow/
    @action(['DELETE'], detail=True)
    def unfollow(self, request, pk):
        following_user = self.get_object()
        user = request.user
        account = user.followers.filter(following=following_user)
        if following_user == user:
            return Response('You cannot unfollow yourself!', status=400)
        if not account.exists():
            return Response('You didn\'t followed to this user!', status=400)
        account.delete()
        return Response('Successfully unfollowed!', status=204)


class FollowersApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        queryset = user.followings.all()
        print(queryset, '!!!!!!!!!')
        serializer = serializers.FollowersSerializer(instance=queryset,
                                                     many=True)
        return Response(serializer.data, status=200)


class FollowingsApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        queryset = user.followers.all()
        serializer = serializers.FollowingsSerializer(instance=queryset,
                                                      many=True).data
        return Response(serializer, status=200)


# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserListSerializer
#     permission_classes = (permissions.AllowAny,)
#     filter_backends = (SearchFilter,)
#     search_fields = ('username', 'email')

# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserDetailSerializer
#     permission_classes = (permissions.IsAuthenticated,)




