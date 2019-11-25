"""
******************************************************************************
* Purpose: purpose is to define the urls for the API views
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
from .views import LoginAPIView, RegisterAPIView, HelloView, activate, DetailsView, PasswordForgotAPIView, \
    PasswordResetAPIView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
 path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
 path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
 path('register/', RegisterAPIView.as_view(), name='register'),
 path('activate/<token>/', activate, name='email-activation'),
 path('login/', LoginAPIView.as_view(), name='login'),
 path('forgot-password/', PasswordForgotAPIView.as_view(), name='forgot-password'),
 path('reset-password/<token>/', PasswordResetAPIView.as_view(), name='reset-password'),
 path('hello/', HelloView.as_view(), name='hello user'),
 path('details/', DetailsView.as_view(), name='details')

]
