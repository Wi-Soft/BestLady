from django.shortcuts import render
from .models import Header, Product, Hair, Nail



# Create your views here.

def home(request):
    products = Product.objects.all()
    hairs = Hair.objects.all()
    nails = Nail.objects.all()
    return render(request, 'home.html', {'products': products, 'hairs': hairs, 'nails': nails})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def header(request):
    return render(request, 'header.html')

def hair_list(request):
    hairs = Hair.objects.all()
    return render(request, 'hair.html', {'hairs': hairs})

def nail_list(request):
    nails = Nail.objects.all()
    return render(request, 'nail.html', {'nails': nails})

def buy(request):
    return render(request, 'buy.html')

def data_structure(request):
    return render(request, 'data_structure.html')
