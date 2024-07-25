import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment

def generate_data():
    user_model = get_user_model()
    users = []

    # Create 5 users
    for i in range(5):
        characters = str(i) + string.ascii_letters + string.digits
        number = ''.join(random.choice(characters) for _ in range(5))
        email_number = ''.join(random.choice(characters) for _ in range(7))
        username = f'user{number}'
        email = f'user{email_number}@example.com'
        password = 'password123'
        user = user_model.objects.create_user(username=username, email=email, password=password)
        users.append(user)

    # Create 10 blog posts for each user
    for user in users:
        for j in range(10):
            post_title = f'Post {j} by {user.username}'
            post_content = f'This is the content of {post_title}'
            post = Post.objects.create(title=post_title, content=post_content, author=user)

            # Create 10 comments for each post
            for k in range(10):
                comment_content = f'This is comment {k} on {post_title}'
                commenter = random.choice(users)
                Comment.objects.create(post=post, author=commenter, content=comment_content)

class Command(BaseCommand):
    help = 'Generate test data with 5 users, each creating 10 blog posts, and each post having 10 comments.'

    def handle(self, *args, **kwargs):
        generate_data()
        self.stdout.write(self.style.SUCCESS('Data generation complete!'))
