from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Header, Product, Hair, Nail


CATALOG_MODELS = {
    'product': Product,
    'hair': Hair,
    'nail': Nail,
}

CATALOG_LABELS = {
    'product': 'Cosmetics',
    'hair': 'Hair',
    'nail': 'Nails',
}


def _get_cart(request):
    return request.session.setdefault('cart', {})


def _get_catalog_item(item_type, pk):
    model = CATALOG_MODELS.get(item_type)
    if model is None:
        raise Http404("Catalog item type not found")
    return get_object_or_404(model, pk=pk)


def _cart_key(item_type, pk):
    return f'{item_type}:{pk}'


def _redirect_after_cart_action(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    return redirect(next_url or 'cart_detail')


def _cart_entries(request):
    cart = _get_cart(request)
    entries = []
    total = 0
    invalid_keys = []

    for key, quantity in cart.items():
        try:
            item_type, raw_pk = key.split(':', 1)
            model = CATALOG_MODELS[item_type]
            item = model.objects.get(pk=raw_pk)
            quantity = max(1, int(quantity))
        except (KeyError, ValueError, ObjectDoesNotExist):
            invalid_keys.append(key)
            continue

        subtotal = item.price * quantity
        total += subtotal
        entries.append({
            'key': key,
            'item_type': item_type,
            'label': CATALOG_LABELS[item_type],
            'item': item,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    for key in invalid_keys:
        cart.pop(key, None)

    if invalid_keys:
        request.session.modified = True

    return entries, total

# Create your views here.

def home(request):
    products = Product.objects.all()
    hairs = Hair.objects.all()
    nails = Nail.objects.all()
    return render(request, 'home.html', {'products': products, 'hairs': hairs, 'nails': nails})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.exclude(pk=product.pk)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

def about(request):
    return render(request, 'about.html')

def header(request):
    return render(request, 'header.html')

def database(request):
    return render(request, 'database.html')


def buy(request):
    return render(request, 'buy.html')

def data_structure(request):
    return render(request, 'data_structure.html')


def cart_detail(request):
    entries, total = _cart_entries(request)
    return render(request, 'cart.html', {
        'cart_entries': entries,
        'cart_total': total,
    })


@require_POST
def cart_add(request, item_type, pk):
    _get_catalog_item(item_type, pk)
    cart = _get_cart(request)
    key = _cart_key(item_type, pk)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    quantity = max(1, min(quantity, 99))
    cart[key] = int(cart.get(key, 0)) + quantity
    request.session.modified = True
    return _redirect_after_cart_action(request)


@require_POST
def cart_update(request, item_type, pk):
    _get_catalog_item(item_type, pk)
    cart = _get_cart(request)
    key = _cart_key(item_type, pk)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, 99)

    request.session.modified = True
    return redirect('cart_detail')


@require_POST
def cart_remove(request, item_type, pk):
    cart = _get_cart(request)
    cart.pop(_cart_key(item_type, pk), None)
    request.session.modified = True
    return redirect('cart_detail')


@require_POST
def cart_clear(request):
    request.session['cart'] = {}
    return redirect('cart_detail')


# views.py
def services(request):
    hairs = Hair.objects.all()
    nails = Nail.objects.all()
    return render(request, 'services.html', {
        'hairs': hairs,
        'nails': nails
    })
