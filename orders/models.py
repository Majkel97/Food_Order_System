from django.db import models
from django.contrib.auth.models import User


class MenuType(models.Model):
    """
    Model to represent types of menu items.

    Attributes:
        id (BigAutoField): The unique identifier for the menu type.
        name (CharField): The name of the menu type (e.g., Pizza, Pasta, Drinks).
        description (CharField, optional): A brief description of the menu type.
    """

    TYPE_CHOICES = (
        ("Pizza", "Pizza"),
        ("Pasta", "Pasta"),
        ("Drinks", "Drinks"),
    )

    # id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)
    name = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "menu_type"

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Model to represent menu items.

    Attributes:
        id (BigAutoField): The unique identifier for the menu item.
        name (CharField): The name of the menu item.
        price (DecimalField): The price of the menu item.
        type (ForeignKey): The type of menu item (related to MenuType).
        image (ImageField, optional): An optional image for the menu item.
        ingredients (CharField): The ingredients used in the menu item.
        status (CharField): The availability status of the menu item (A for Available, U for Unavailable).
    """

    MENU_STATUS_CHOICES = (
        ("A", "Available"),
        ("U", "Unavailable"),
    )

    # id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.ForeignKey(MenuType, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    ingredients = models.CharField(max_length=500)
    status = models.CharField(max_length=1, choices=MENU_STATUS_CHOICES)

    class Meta:
        db_table = "menu"

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        """
        Get the menu item's image URL.
        """
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    """
    Model to represent customer orders.

    Attributes:
        id (BigAutoField): The unique identifier for the order.
        customer (ForeignKey): The customer who placed the order (related to User).
        date (DateTimeField): The date and time when the order was placed.
        status (BooleanField): The status of the order (True for completed, False for pending).
        transaction (CharField, optional): The transaction ID for the order (if applicable).
    """

    # id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    transaction = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "order"

    @property
    def cart_total(self):
        """
        Get the total cost of items in the order.
        """
        order_items = self.order_details.all()
        total = sum([item.total for item in order_items])
        return total

    @property
    def cart_items(self):
        """
        Get the total number of items in the order.
        """
        order_items = self.order_details.all()
        total = sum([item.no_of_serving for item in order_items])
        return total


class OrderDetails(models.Model):
    """
    Model to represent the details of items in an order.

    Attributes:
        id (BigAutoField): The unique identifier for the order details.
        order (ForeignKey): The order to which the item belongs (related to Order).
        menu (ForeignKey): The menu item included in the order (related to Menu).
        amount (DecimalField, optional): The amount (price) for the menu item in the order.
        no_of_serving (IntegerField): The number of servings of the menu item in the order.
    """

    # id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order_details",
    )
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    no_of_serving = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        db_table = "order_details"

    @property
    def total(self):
        """
        Calculate the total cost of the item in the order.
        """
        total = self.menu.price * self.no_of_serving
        return total
