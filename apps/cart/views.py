from django.core.paginator import Paginator
from django.db.models import Count, F, Sum
from django.shortcuts import render

from apps.cart.models import CartItem
from apps.store.models import Product
from apps.users.models import User

from .models import Order


def get_pending_orders(request):
    # Fetch only pending orders
    orders = Order.objects.filter(status="PENDING").order_by("-id")
    paginator = Paginator(orders, 3)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "orders/pending.html", {"page_obj": page_obj})


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    cart = order.cart
    cart_items = cart.items.all()
    greatTotal = 0
    for item in cart_items:
        total = item.product.price * item.quantity
        greatTotal += total

    context = {
        "cart_items": cart_items,
        "greatTotal": greatTotal,
    }

    return render(request, "orders/order_details.html", context)


def deliver_order(request):
    orders = Order.objects.all().filter(status="Delivered").order_by("-id")
    paginator = Paginator(orders, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "orders/delivered.html", {"page_obj": page_obj})


def dashboard(request):
    top_products = Product.objects.annotate(
        total_sold=Sum("cartitem__quantity")
    ).order_by("-total_sold")[:10]
    least_sold_products = Product.objects.annotate(
        total_sold=Sum("cartitem__quantity")
    ).order_by("total_sold")[:10]
    top_users = User.objects.annotate(order_count=Count("orders")).order_by(
        "-order_count"
    )[:10]
    total_earnings = (
        CartItem.objects.annotate(
            earnings=F("quantity") * F("product__price")
        ).aggregate(total_earnings=Sum("earnings"))["total_earnings"]
        or 0
    )
    # stock = Product.objects.annotate(stocks=)

    products_stock = (
        Product.objects.filter(stock__gt=0).values("name", "stock").order_by("-stock")
    )

    for product in products_stock:
        print(f"{product['name']}: {product['stock']} in stock")

    context = {
        "products_stock": products_stock,
        "top_users": top_users,
        "top_products": top_products,
        "least_sold_products": least_sold_products,
        "total_earnings": total_earnings,
    }

    return render(request, "orders/dashboard.html", context)
