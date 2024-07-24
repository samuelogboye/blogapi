from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

class PostTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        for i in range(15):
            Post.objects.create(title=f'Test Post {i}', content=f'This is test post {i}.', author=self.user)

    def test_create_post_success(self):
        url = reverse('post-create')
        response = self.client.post(url, data={
            'title': 'New Post',
            'content': 'This is a new post.'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 16)
        self.assertEqual(response.data['authorId'], self.user.id)

    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('post-create')
        response = self.client.post(url, data={
            'title': 'New Post',
            'content': 'This is a new post.'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_post_list(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # Assuming default page size is 10

        response = self.client.get(url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Remaining 5 posts on page 2

    def test_retrieve_post_detail(self):
        post = Post.objects.first()
        url = reverse('post-detail', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post.title)

    def test_update_post_success(self):
        post = Post.objects.first()
        url = reverse('post-update', args=[post.id])
        response = self.client.put(url, data={
            'title': 'Updated Post',
            'content': 'This is an updated post.'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Post')

    def test_update_post_unauthorized(self):
        post = Post.objects.first()
        new_user = get_user_model().objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        self.client.force_authenticate(user=new_user)
        url = reverse('post-update', args=[post.id])
        response = self.client.put(url, data={
            'title': 'Updated Post',
            'content': 'This is an updated post.'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_success(self):
        post = Post.objects.first()
        url = reverse('post-delete', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 14)

    def test_delete_post_unauthorized(self):
        post = Post.objects.first()
        new_user = get_user_model().objects.create_user(username='newuser', email='newuser@example.com', password='newpass123')
        self.client.force_authenticate(user=new_user)
        url = reverse('post-delete', args=[post.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
