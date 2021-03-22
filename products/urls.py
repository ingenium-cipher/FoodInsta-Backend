from . import views
from django.urls import path

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='new-post'),
    path('list/', views.PostListView.as_view(), name='post-list')
]