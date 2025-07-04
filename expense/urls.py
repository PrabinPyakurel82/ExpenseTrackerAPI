from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .views import RegisterView,LoginView,RefreshTokenView,ExpenseIncomeViewset


router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewset, basename='expense')


urlpatterns = [
    path('auth/register/',RegisterView.as_view(),name='register'),
    path('auth/login/',LoginView.as_view(),name='token-obtain'),
    path('auth/refresh/',RefreshTokenView.as_view(),name='token-refresh'),
    path('',include(router.urls))

]
