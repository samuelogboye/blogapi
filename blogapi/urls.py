from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/",
        include(
            [
                path('users/', include('users.urls')),
                path('', include('posts.urls')),
                path('', include('comments.urls')),
                path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            ]
        ),
    ),
]
