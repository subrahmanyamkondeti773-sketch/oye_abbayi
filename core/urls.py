from django.urls import path
from . import views
from .views import profile_view

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.BuyNowView.as_view(), name='buy_now'),
    path('update-cart/<int:item_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    path('order-confirm/<int:order_id>/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('profile/', profile_view, name='profile'),    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
