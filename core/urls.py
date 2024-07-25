from django.urls import path
from .views import trigger_data_generation

urlpatterns = [
    # Your other URL patterns
    path('seed-data/', trigger_data_generation, name='generate-data'),
]
