from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login/', views.UserLoginAPI.as_view(), name='user-login'),
    path('register/', views.UserRegisterAPI.as_view(), name='user-register'),
    path('token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.UserProfileAPI.as_view(), name='user-profile')
]