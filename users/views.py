from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer
from .tasks import send_registration_email


@extend_schema(tags=['Users'], summary='Register a new user')
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Send a welcome email using Celery
        subject = "Welcome to Our Platform!"
        message = f"Hello {user.username},\n\nThank you for registering on our platform."
        recipient_list = [user.email]
        send_registration_email.delay(subject, message, recipient_list)

@extend_schema(tags=['Users'], summary='Authenticate user and return a token')
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            user = self.get_user(request)
            # Send a login notification email
            subject = "Login Notification"
            message = f"Hello {user.username},\n\nYou have successfully logged into your account."
            recipient_list = [user.email]
            send_registration_email.delay(subject, message, recipient_list)

        return response

    def get_user(self, request):
        """
        Helper method to retrieve the user based on request data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.user
   
@extend_schema(tags=['Users'], summary='Get user profile (Authenticated)') 
class ProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
