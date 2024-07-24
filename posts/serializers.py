from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    authorId = serializers.PrimaryKeyRelatedField(source='author.id', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'authorId', 'createdAt', 'updatedAt']
        read_only_fields = ['authorId', 'createdAt', 'updatedAt']
