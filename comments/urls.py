from django.urls import path
from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path('posts/<int:postId>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:id>/', CommentDetailView.as_view(), name='comment-detail'),
]
