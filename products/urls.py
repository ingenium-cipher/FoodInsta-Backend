from . import views
from django.urls import path

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='new-post')
]