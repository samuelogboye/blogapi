from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .management.commands.generate_data import generate_data


def return_home_to_docs(request):
    return redirect("swagger-schema")

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only allow admin users to trigger this endpoint
def trigger_data_generation(request):
    generate_data()
    return JsonResponse({'status': 'Data generation complete!'})
