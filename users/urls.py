from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/individual/', views.IndividualRegisterView.as_view(), name='individual-register'),
    path('register/restaurant/', views.RestaurantRegisterView.as_view(), name='restaurant-register'),
    path('register/ngo/', views.NGORegisterView.as_view(), name='ngo-register'),
    path('profile', views.UserProfileView.as_view(), name='user-profile'),
    path('city_list', views.CityListView.as_view(), name='city-list'),
    path('ngo_list', views.NGOListView.as_view(), name='ngo-list')
]