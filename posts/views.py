from rest_framework import permissions, pagination, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter

class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostView(APIView):
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        elif self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @extend_schema(tags=['Posts'], summary='Retrieve all posts (Paginated)')
    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        return self.list(request)

    @extend_schema(tags=['Posts'], summary='Create a new post (Authenticated)')
    def post(self, request):
        return self.create(request)

    @extend_schema(tags=['Posts'], summary='Update a post by ID (Authenticated & Author only)')
    def put(self, request, pk):
        return self.update(request, pk)

    @extend_schema(tags=['Posts'], summary='Delete a post by ID (Authenticated & Author only)')
    def delete(self, request, pk):
        return self.destroy(request, pk)

    def list(self, request):
        queryset = Post.objects.all().order_by('createdAt')
        
        # Apply filters
        filter_backends = self.filter_backends
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
            
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
