from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostViewSet)
                # .../posts/  -> GET(list), POST(create)
                # .../posts/<id>/  -> GET(retrieve), PUT/PATCH(update),
#                                               DELETE(destroy)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('likes/', views.LikeCreateView.as_view()),
    path('likes/<int:pk>/', views.LikeDeleteView.as_view()),

    # path('posts/', views.PostListCreateView.as_view()), # Урлы женериксов
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
]

# TODO followers
# TODO deploy
# TODO search, filter, pagination


