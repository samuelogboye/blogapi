from django.urls import path
from .views import CommentListView, CommentCreateView, CommentDetailView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('posts/<int:postId>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<int:postId>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
