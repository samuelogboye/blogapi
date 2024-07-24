from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.IntegerField(source='post.id', read_only=True)
    authorId = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'postId', 'authorId', 'content', 'createdAt', 'updatedAt']
        read_only_fields = ['postId', 'authorId', 'createdAt', 'updatedAt']
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
