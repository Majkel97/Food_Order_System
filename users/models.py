from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    """
    Model to represent customer information.

    Attributes:
        username (OneToOneField): The linked User model representing the customer's username.
        phone_number (CharField): The customer's phone number.
        postal_code (CharField): The customer's postal code (zip code).
        city (CharField): The customer's city.
        street (CharField): The customer's street.
        number (CharField): The customer's house or apartment number.
    """

    username = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    phone_number = models.CharField(
        max_length=12, null=False, blank=False, unique=True, verbose_name="Phone number"
    )
    postal_code = models.CharField(max_length=6, verbose_name="Zip code")
    city = models.CharField(max_length=50, verbose_name="City")
    street = models.CharField(max_length=50, verbose_name="Street")
    number = models.CharField(max_length=50, verbose_name="Number")

    class Meta:
        db_table = "customers"

    def __str__(self):
        """
        Get a string representation of the customer using their username.
        """
        return str(self.username)
