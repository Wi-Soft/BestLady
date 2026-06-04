from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.product_list, name='products'),
    path('header/', views.header, name='header'),
    path('buy/', views.buy, name='buy'),
    path('data-structure/', views.data_structure, name='data_structure'),
    path('services/', views.services, name='services'),
    path('database/', views.database, name='database')
]