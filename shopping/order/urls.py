from django.urls import path
from . import views
urlpatterns = [
    path("create/",views.OrderAPIView.as_view(),name="order_create"),
    path("history/",views.history_order,name="order_history"),
    path('items/', views.OrderItemAPIView.as_view(), name='order_items'),
    path('items/<int:pk>/', views.OrderItemDetailAPIView.as_view(), name='order_item_detail'),
]

    
