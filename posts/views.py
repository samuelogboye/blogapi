from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter

@extend_schema(tags=['Posts'], summary='Retrieve all posts (Paginated)')
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('createdAt')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

@extend_schema(tags=['Posts'], summary='Create a new post (Authenticated)')
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@extend_schema(tags=['Posts'], summary='Retrieve a single post by ID')
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@extend_schema(tags=['Posts'], summary='Update a post by ID (Authenticated & Author only)')
class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

@extend_schema(tags=['Posts'], summary='Delete a post by ID (Authenticated & Author only)')
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
