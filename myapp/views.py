from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})


def about(request):
    return render(request, 'about.html')