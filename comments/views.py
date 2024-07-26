from rest_framework import status, permissions, pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from posts.models import Post
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly

class CommentPagination(pagination.PageNumberPagination):
    page = 10  # default page size
    page_size_query_param = 'page'
    max_page_size = 100
    
class CommentView(APIView):
    pagination_class = CommentPagination
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        elif self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    @extend_schema(tags=['Comments'], summary='Retrieve all comments for a post (Paginated)')
    def get(self, request, post_id=None, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request, post_id)

    @extend_schema(tags=['Comments'], summary='Create a new comment on a post (Authenticated)')
    def post(self, request, post_id):
        return self.create(request, post_id)

    @extend_schema(tags=['Comments'], summary='Update a comment by ID (Authenticated & Author only)')
    def put(self, request, pk):
        return self.update(request, pk)

    @extend_schema(tags=['Comments'], summary='Delete a comment by ID (Authenticated & Author only)')
    def delete(self, request, pk):
        return self.destroy(request, pk)

    def list(self, request, post_id):
        get_object_or_404(Post, id=post_id)
        queryset = Comment.objects.filter(post_id=post_id).order_by('createdAt')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def paginate_queryset(self, queryset):
    #     paginator = self.pagination_class()
    #     return paginator.paginate_queryset(queryset, self.request, view=self)

    # def get_paginated_response(self, data):
    #     paginator = self.pagination_class()
    #     return paginator.get_paginated_response(data)