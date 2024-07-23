from django.db import models
from django.conf import settings
from posts.models import Post

class Comment(models.Model):
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    authorId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
