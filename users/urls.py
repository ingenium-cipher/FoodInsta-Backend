from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    # path('profile/', views.UserProfileAPI.as_view(), name='user-profile')
]