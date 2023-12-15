from django.urls import path
from app.views import *

urlpatterns = [
    # Shop urls
    path('products/', ProductListView.as_view(), name='products-view'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-view'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('addCart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # User urls
    path('users/', UserListView.as_view(), name='user_list'),
    path('user/register1/', RegisterSimpleView.as_view(), name='register-simple'),
    path('user/register2/', RegisterAdminView.as_view(), name='register-admin'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),

    path('form.html/', ItemView.as_view()),
]
