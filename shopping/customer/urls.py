from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.MyLogoutView.as_view(), name="logout"),
    path("shopping_cart/", views.shopping_cart, name="shopping_cart"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('verify_code/', views.Verify_code.as_view(), name='verify_code'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('address/api/',views.AddressAPIView.as_view(),name="address_list"),
    path('address/api/<int:pk>/', views.AddressDetailAPIview.as_view(), name='address_detail'),
  
   
]
