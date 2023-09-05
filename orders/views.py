from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from orders.models import Menu, Order, OrderDetails
import json
import datetime


def index(request):
    """
    Display the index page, including the user's shopping cart information if authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'orders/index.html' template with the appropriate context.
    """

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer.username, status=False
        )
        cartItems = order.cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = []

    context = {"menu": menu, "cartItems": cartItems}
    return render(request, "orders/index.html", context)


def menu(request):
    """
    Display the menu page, including menu items and the user's shopping cart information if authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'orders/menu.html' template with the appropriate context.
    """

    menu = Menu.objects.filter(status="A").order_by("type", "price")

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer.username, status=False
        )
        cartItems = order.cart_items
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = []

    context = {"menu": menu, "cartItems": cartItems}
    return render(request, "orders/menu.html", context)


@login_required(login_url="signin")
def cart(request):
    """
    Display the user's shopping cart, including the cart items and order details if authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'orders/cart.html' template with the appropriate context.
    """

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer.username, status=False
        )
        cartItems = order.cart_items
        items = order.order_details.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = []

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "orders/cart.html", context)


@login_required(login_url="signin")
def checkout(request):
    """
    Display the checkout page, including the user's shopping cart and order details if authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'orders/checkout.html' template with the appropriate context.
    """

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer.username, status=False
        )
        cartItems = order.cart_items
        items = order.order_details.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = []

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "orders/checkout.html", context)


@login_required(login_url="signin")
def updateItem(request):
    """
    Handle updates to items in the user's shopping cart based on the provided action.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data.

    Returns:
        JsonResponse: JSON response indicating the result of the update.
    """
    data = json.loads(request.body)
    dishId = data["dishId"]
    action = data["action"]

    customer = request.user.customer
    dish = Menu.objects.get(id=dishId)
    order, created = Order.objects.get_or_create(
        customer=customer.username, status=False
    )
    orderItem, created = OrderDetails.objects.get_or_create(order=order, menu=dish)

    if action == "add":
        orderItem.no_of_serving += 1
    elif action == "remove":
        orderItem.no_of_serving -= 1
    elif action == "delete":
        orderItem.no_of_serving = 0

    orderItem.save()

    if orderItem.no_of_serving <= 0:
        orderItem.delete()

    return JsonResponse("Item was updated", safe=False)


@login_required(login_url="signin")
def procesOrder(request):
    """
    Process the user's order and mark it as paid if the total matches.

    Args:
        request (HttpRequest): The HTTP request object containing JSON data.

    Returns:
        JsonResponse: JSON response indicating the result of the order processing.
    """
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer_table
        order, created = Order.objects.get_or_create(
            customer_id=customer.customer_username, order_status=False
        )
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total()):
            order.order_status = True
        order.save()

    return JsonResponse("Payment complete!", safe=False)
