from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Customer


class SignUpForm(UserCreationForm):
    """
    Form for user registration.

    Attributes:
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        email (EmailField): The user's email address.
    """

    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="First name"
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="Last name"
    )
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        label="Email address",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        )


class AddressForm(forms.ModelForm):
    """
    Form for customer address information.

    Attributes:
        phone_number (CharField): The customer's phone number.
        city (CharField): The city where the customer resides.
        postal_code (CharField): The postal code (zip code) of the customer's location.
        street (CharField): The street where the customer lives.
        number (CharField): The house or apartment number of the customer.
    """

    class Meta:
        model = Customer
        fields = (
            "phone_number",
            "city",
            "postal_code",
            "street",
            "number",
        )
