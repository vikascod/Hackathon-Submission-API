from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView


User = get_user_model()

# Create your views here.
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"Error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"Response": token.key}, status=status.HTTP_200_OK)
        
        return Response({"Error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    

# class UserRegistrationAPIView(CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"Response": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
