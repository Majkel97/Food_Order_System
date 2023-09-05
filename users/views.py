from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from users.models import Customer
from users.forms import SignUpForm, AddressForm


def signup(request):
    """
    Handle user signup and address creation.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'index' page upon successful signup or
        renders the signup form if the request method is not POST.
    """

    if request.method == "POST":
        formset = SignUpForm(request.POST)
        address_formset = AddressForm(request.POST)
        if formset.is_valid() and address_formset.is_valid():
            user = formset.save()
            address_data = address_formset.cleaned_data
            Customer.objects.create(
                username=user,
                phone_number=address_data["phone_number"],
                postal_code=address_data["postal_code"],
                city=address_data["city"],
                street=address_data["street"],
                number=address_data["number"],
            )
            return redirect("index")
    else:
        formset = SignUpForm()
        address_formset = AddressForm()

    context = {"formset": formset, "address_formset": address_formset}
    return render(request, "users/signup.html", context)


def signin(request):
    """
    Handle user sign-in.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'index' page upon successful sign-in or
        renders the sign-in form if the request method is not POST.
    """

    if request.method == "POST":
        formset = AuthenticationForm(data=request.POST)
        if formset.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        formset = AuthenticationForm()

    context = {"formset": formset}
    return render(request, "users/login.html", context)


def logout_view(request):
    """
    Log the user out and redirect to the 'index' page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'index' page after logging the user out.
    """
    logout(request)
    return redirect("index")
