from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import Resident


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password.'}, status=400)
    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=404)
    login(request, user)
    return Response({'message': 'User logged in successfully.'}, status=200)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'User logged out successfully.'}, status=200)
