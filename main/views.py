from rest_framework import generics, permissions, mixins
from rest_framework.viewsets import ModelViewSet

from .models import Category, Post, Comment, Like
from . import serializers
from .permissions import IsAuthorOrAdmin, IsAuthor, IsAuthorOrAdminOrPostOwner


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(),
                    IsAuthorOrAdminOrPostOwner()]
        return [permissions.AllowAny()]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # Удалять может только админ или автор поста
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]
        # Обновлять может только автор поста
        elif self.action in ('update', 'partial_update'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        # Просматривать могут все, но создовать только аутентифицированный пользователь
        return [permissions.IsAuthenticatedOrReadOnly()]


class LikeCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthor)


# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return serializers.PostListSerializer
#         return serializers.PostCreateSerializer
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#
#     def get_permissions(self):
#         if self.request.method == 'DELETE':
#             return (permissions.IsAuthenticated(),
#                     IsAuthorOrAdmin())
#         elif self.request.method in ('PUT', 'PATCH'):
#             return (permissions.IsAuthenticated(),
#                     IsAuthor())
#         return [permissions.AllowAny()]
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return serializers.PostCreateSerializer
#         return serializers.PostDetailSerializer



