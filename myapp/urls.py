from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('header/', views.header, name='header'),
    path('buy/', views.buy, name='buy'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<str:item_type>/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/update/<str:item_type>/<int:pk>/', views.cart_update, name='cart_update'),
    path('cart/remove/<str:item_type>/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('data-structure/', views.data_structure, name='data_structure'),
    path('services/', views.services, name='services'),
    path('database/', views.database, name='database')
]
