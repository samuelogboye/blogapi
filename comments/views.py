from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

@extend_schema(tags=['Comments'], summary='Retrieve all comments for a post (Paginated)')
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['postId']
        get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post_id=post_id).order_by('createdAt')

@extend_schema(tags=['Comments'], summary='Create a new comment on a post (Authenticated)')
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['postId']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

@extend_schema(tags=['Comments'], summary='Get a Comment by ID')
class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema(tags=['Comments'], summary='Update a comment by ID (Authenticated & Author only)')
class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

@extend_schema(tags=['Comments'], summary='Delete a comment by ID (Authenticated & Author only)')
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
