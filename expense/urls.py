from django.urls import path

from .views import RegisterView,LoginView,RefreshTokenView

urlpatterns = [
    path('auth/register/',RegisterView.as_view(),name='register'),
    path('auth/login/',LoginView.as_view(),name='token_obtain'),
    path('auth/refresh/',RefreshTokenView.as_view(),name='token-refresh'),

]
