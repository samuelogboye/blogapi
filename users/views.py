from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.utils.timezone import localtime
import logging
from datetime import datetime
from .serializers import UserSerializer
from .tasks import send_notification_via_email

logger = logging.getLogger(__name__)

@extend_schema(tags=['Users'], summary='Register a new user')
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Send a welcome email using Celery
        subject = "Welcome to Our Platform!"
        recipient_list = [user.email]
        template = "register_notification.html"
        context = {
            "username": user.username,
            "year": datetime.now().year,
            "dashboard_url": "www.google.com"
        }
        send_notification_via_email.delay(subject, recipient_list, template, context)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed as exc:
            # Customize the error message for incorrect credentials
            raise AuthenticationFailed("Incorrect username or password.")

@extend_schema(tags=['Users'], summary='Authenticate user and return a token')
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            logger.debug(f"Request data: {request.data}")
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                # Retrieve the user from the serializer
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.user

                # Extract additional context
                ip_address = self.get_ip_address(request)
                device_type = self.get_device_type(request)
                login_time = localtime().strftime("%m/%d/%Y, %I:%M %p")


                # Send a login notification email
                subject = "Login Notification"
                recipient_list = [user.email]
                context = {
                    "username": user.username,
                    "ip_address": ip_address,
                    "device_type": device_type,
                    "login_time": login_time,
                }
                template = "login_notification.html"
                send_notification_via_email.delay(subject, recipient_list, template, context)

            return response
        except AuthenticationFailed as e:
            logger.error(f"Authentication failed: {str(e)}")
            return Response(
                {"error_code": "ERR_003", "error": "Authentication Error", "detail": str(e)},
                status=401,
            )
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            return Response(
                {"error_code": "ERR_500", "error": "Internal Server Error", "detail": "An unexpected error occurred."},
                status=500,
            )
    
    def get_ip_address(self, request):
        """Extract the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]  # Take the first IP in the list
        return request.META.get('REMOTE_ADDR', 'Unknown')

    def get_device_type(self, request):
        """Extract the device type from the User-Agent string."""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'windows' in user_agent:
            return "Windows"
        elif 'mac' in user_agent:
            return "MacOS"
        elif 'iphone' in user_agent or 'ipad' in user_agent:
            return "iOS"
        elif 'android' in user_agent:
            return "Android"
        elif 'linux' in user_agent:
            return "Linux"
        return user_agent # Default back to the exact device type #"Unknown"
        
@extend_schema(tags=['Users'], summary='Get user profile (Authenticated)') 
class ProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
