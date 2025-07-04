from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


from .models import ExpenseIncome
from .serializers import UserSerializer, ExpenseIncomeDetailSerializer,ExpenseIncomeListSerializer
from .permissions import IsOwnerOrSuperuser
from .pagination import MyPagination


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


class ExpenseIncomeViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrSuperuser]
    pagination_class = MyPagination


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all()
        return ExpenseIncome.objects.filter(user=user)
    

    def get_object(self):
        obj = get_object_or_404(ExpenseIncome, pk=self.kwargs['pk'])
        if self.request.user != obj.user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this record.")
        return obj
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExpenseIncomeListSerializer
        return ExpenseIncomeDetailSerializer
    
        
