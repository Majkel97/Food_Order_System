from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Customer
from orders.models import Menu, OrderDetails, Order


class MenuViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some test menu items
        self.menu_item1 = Menu.objects.create(
            name="Item 1", price=10.00, status="A", type="Type 1"
        )

        self.menu_item2 = Menu.objects.create(
            name="Item 2", price=15.00, status="A", type="Type 2"
        )

    def test_menu_view_authenticated_user(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Create a customer for the user
        customer = Customer.objects.create(user=self.user)

        # Get the menu page
        response = self.client.get(reverse("menu"))  # Use the actual URL name

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the menu items are present in the context
        self.assertIn("menu", response.context)
        self.assertEqual(
            list(response.context["menu"]), [self.menu_item1, self.menu_item2]
        )

        # Check if the user's cart items are present in the context
        self.assertIn("cartItems", response.context)

    def test_menu_view_unauthenticated_user(self):
        # Log out any previously logged-in user (if any)
        self.client.logout()

        # Get the menu page
        response = self.client.get(reverse("menu"))  # Use the actual URL name

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the menu items are present in the context
        self.assertIn("menu", response.context)
        self.assertEqual(
            list(response.context["menu"]), [self.menu_item1, self.menu_item2]
        )

        # Check if the context has the expected values for an unauthenticated user
        self.assertIn("cartItems", response.context)
        self.assertEqual(response.context["cartItems"], [])


class UpdateItemViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create some test menu items
        self.menu_item1 = Menu.objects.create(
            name="Item 1", price=10.00, status="A", type="Type 1"
        )

        # Create a customer for the user
        self.customer = Customer.objects.create(user=self.user)

        # Create an order for the customer
        self.order = Order.objects.create(customer=self.customer, status=False)

        # Create an order item for the menu item
        self.order_item = OrderDetails.objects.create(
            order=self.order, menu=self.menu_item1, no_of_serving=2
        )

    def test_update_item_add(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the update action (add)
        action = "add"

        # Define the data to be sent in the request
        data = {"dishId": self.menu_item1.id, "action": action}

        # Make a POST request to the updateItem view
        response = self.client.post(
            reverse("update_item"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the order item was updated correctly (e.g., no_of_serving increased by 1)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.no_of_serving, 3)

    def test_update_item_remove(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the update action (remove)
        action = "remove"

        # Define the data to be sent in the request
        data = {"dishId": self.menu_item1.id, "action": action}

        # Make a POST request to the updateItem view
        response = self.client.post(
            reverse("update_item"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the order item was updated correctly (e.g., no_of_serving decreased by 1)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.no_of_serving, 1)

    def test_update_item_delete(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the update action (delete)
        action = "delete"

        # Define the data to be sent in the request
        data = {"dishId": self.menu_item1.id, "action": action}

        # Make a POST request to the updateItem view
        response = self.client.post(
            reverse("update_item"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the order item was deleted
        with self.assertRaises(OrderDetails.DoesNotExist):
            self.order_item.refresh_from_db()


class ProcessOrderViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_process_order_authenticated_user(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Create a customer for the user
        customer = Customer.objects.create(user=self.user)

        # Define the data to be sent in the request (e.g., with a matching total)
        data = {"form": {"total": "10.00"}}

        # Make a POST request to the processOrder view
        response = self.client.post(
            reverse("process_order"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the order's status is updated to True
        order = Order.objects.get(customer=customer, status=False)
        self.assertTrue(order.order_status)
        self.assertIsNotNone(order.transaction_id)

    def test_process_order_authenticated_user_invalid_total(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Create a customer for the user
        customer = Customer.objects.create(user=self.user)

        # Define the data to be sent in the request (e.g., with an invalid total)
        data = {"form": {"total": "15.00"}}

        # Make a POST request to the processOrder view
        response = self.client.post(
            reverse("process_order"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the order's status remains False
        order = Order.objects.get(customer=customer, status=False)
        self.assertFalse(order.order_status)

    def test_process_order_unauthenticated_user(self):
        # Log out any previously logged-in user (if any)
        self.client.logout()

        # Define the data to be sent in the request (e.g., with a matching total)
        data = {"form": {"total": "10.00"}}

        # Make a POST request to the processOrder view
        response = self.client.post(
            reverse("process_order"), data, content_type="application/json"
        )

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
