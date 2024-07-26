from django.urls import path
from .views import PostView

urlpatterns = [
    path('posts', PostView.as_view(), name='post-list-create'),
    path('posts/<int:pk>', PostView.as_view(), name='post-detail-update-delete'),
]
