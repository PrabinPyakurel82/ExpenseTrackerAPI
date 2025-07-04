from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .serializers import UserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"User registered successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(TokenObtainPairView):
    pass

class RefreshTokenView(TokenRefreshView):
    pass
