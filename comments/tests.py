from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post
from .models import Comment

class CommentTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        for i in range(5):
            Comment.objects.create(post=self.post, author=self.user, content=f'This is test comment {i}.')

    def test_create_comment_success(self):
        url = reverse('comment-list-create', args=[self.post.id])
        response = self.client.post(url, data={
            'content': 'This is a new comment.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 6)
        self.assertEqual(response.data['authorId'], self.user.id)

    def test_create_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('comment-list-create', args=[self.post.id])
        response = self.client.post(url, data={
            'content': 'This is a new comment.'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_comment_list(self):
        url = reverse('comment-list-create', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_retrieve_comment_detail(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail-update-delete', args=[comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], comment.content)

    def test_update_comment_success(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail-update-delete', args=[comment.id])
        response = self.client.put(url, data={
            'content': 'Updated comment.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment.')

    def test_update_comment_unauthorized(self):
        comment = Comment.objects.first()
        new_user = get_user_model().objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        self.client.force_authenticate(user=new_user)
        url = reverse('comment-detail-update-delete', args=[comment.id])
        response = self.client.put(url, data={
            'content': 'Updated comment.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_success(self):
        comment = Comment.objects.first()
        url = reverse('comment-detail-update-delete', args=[comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 4)

    def test_delete_comment_unauthorized(self):
        comment = Comment.objects.first()
        new_user = get_user_model().objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        self.client.force_authenticate(user=new_user)
        url = reverse('comment-detail-update-delete', args=[comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

