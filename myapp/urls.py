from . import views
from django.urls import path
from django.conf.urls.static import static



urlpatterns = [   
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.product, name='products'),
]