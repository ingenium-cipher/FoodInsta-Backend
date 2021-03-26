from . import views
from django.urls import path

urlpatterns = [
    path('new/', views.PostCreateView.as_view(), name='new-post'),
    path('list', views.PostListView.as_view(), name='post-list'),
    path('detail', views.PostDetailView.as_view(), name='post-detail'),
    path('new_order/', views.CreateOrderView.as_view(), name='new-order'),
    path('all_posts', views.UserPostListView.as_view(), name='user-post-list'),
    path('all_orders', views.OrderListView.as_view(), name='order-list'),
    path('all_requests', views.RequestListView.as_view(), name='request-list'),
    path('update_order_status/', views.UpdateOrderStatusView.as_view(), name='update-order-status')
]