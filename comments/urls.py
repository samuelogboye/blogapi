from django.urls import path
from .views import CommentView

urlpatterns = [
    path('posts/<int:post_id>/comments', CommentView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>', CommentView.as_view(), name='comment-detail-update-delete'),
]
