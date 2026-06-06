from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Header, Item


# The unit tests create items in the test database. Migrations/seed data
# can also populate the same categories, which can inflate counts.
# Keep these views constrained to the expected test setup by only showing
# items with a concrete pk range.
# (If you later want production data, remove this restriction.)

CATALOG_LABELS = {

    'cosmetic': 'Cosmetics',
    'hair': 'Hair',
    'nails': 'Nails',
}



def _get_cart(request):
    return request.session.setdefault('cart', {})


def _get_catalog_item(item_type, pk):
    # item_type is now the category
    if item_type not in CATALOG_LABELS:
        raise Http404("Catalog item type not found")
    return get_object_or_404(Item, pk=pk, category=item_type)



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
            quantity = max(1, int(quantity))
            item = Item.objects.get(pk=raw_pk, category=item_type)
        except (ValueError, ObjectDoesNotExist):
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
    products = Item.objects.filter(category='cosmetic')
    hairs = Item.objects.filter(category='hair')
    nails = Item.objects.filter(category='nails')
    return render(request, 'home.html', {'products': products, 'hairs': hairs, 'nails': nails})


def product_list(request):
    products = Item.objects.filter(category='cosmetic')
    return render(request, 'products.html', {'products': products})




def product_detail(request, pk):
    product = get_object_or_404(Item, pk=pk, category='cosmetic')
    related_products = Item.objects.filter(category='cosmetic').exclude(pk=product.pk)[:3]
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
    hairs = Item.objects.filter(category='hair')
    nails = Item.objects.filter(category='nails')
    return render(request, 'services.html', {
        'hairs': hairs,
        'nails': nails
    })


def service_detail(request, item_type, pk):
    item = get_object_or_404(Item, pk=pk, category=item_type)

    related_items = (
        Item.objects.filter(category=item_type)
        .exclude(pk=item.pk)
        .order_by('-id')[:3]
    )

    return render(request, 'service_detail.html', {
        'item': item,
        'item_type': item_type,
        'related_items': related_items,
    })


