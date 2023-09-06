# Food_Order_System

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Project Functions](#project-functions-with-visualization)
- [Installation](#instalation)
- [Usage](#usage)

## Introduction

This README provides an overview of a Django project that implements a basic online food ordering system created in April 2022. The project includes features such as user authentication, displaying a menu of food items, managing a shopping cart, and processing orders.

## Project Structure

The project consists of two main Django apps:

1. `orders`: This app handles the core functionality of the food ordering system, including displaying the menu, managing the shopping cart, and processing orders with PayPal integration.
2. `users`: This app manages user authentication and registration.

## Project Functions with visualization

1. Create an account
   
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/1_create_account.png?raw=true"  width="800px" height="auto">

2. Log In

<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/2_log_in.png?raw=true"  width="800px" height="auto">

3. Log Out

4. Show menu
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/3_show_menu.png?raw=true"  width="800px" height="auto">

5. Add products to the cart

6. View cart with edit option (add, remove, delete products)
   
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/4_cart.png?raw=true"  width="800px" height="auto">

7. Show summary
    
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/5_summary.png?raw=true"  width="800px" height="auto">

8. Confirm and pay with PayPal integration (Blik, PayPal, Card, Przelewy24) - Sandbox mode
    
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/6_pay_pal.png?raw=true"  width="800px" height="auto">
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/7_payment_process.png?raw=true"  width="800px" height="auto">
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/8_confrimation_client.png?raw=true"  width="800px" height="auto">
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/9_confirmation_store.png?raw=true"  width="800px" height="auto">
<img src="https://github.com/Majkel97/Food_Order_System/blob/main/img_for_readme/10_transaction_details.png?raw=true"  width="800px" height="auto">

## Instalation

1. Download code from this repository and open it in IDE (for example Visual Studio Code).

2. Create a .env file inside food_order_system folder
   It has to contain the following data:

   ```
   # Replace variable values with your secrets / key / logins

   # Django settings
   DEBUG='TRUE_OR_FALSE'
   SECRET_KEY='YOUR_SECRET_KEY'

   # Database settings
   SQL_ENGINE=django.db.backends.postgresql
   POSTGRES_DB='DATABASE_NAME'
   POSTGRES_PASSWORD='DATABASE_PASSWORD'
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

   # PayPal settings
   PAYPAL_CLIENT_ID = 'YOUR_PAYPAL_CLIENT_ID'
   PAYPAL_CURRENCY = 'CURRENCY'
   ```

3. Make sure you have docker installed and running

4. Run the following commands from the app directory

   ```
   cd .docker
   docker compose build
   ```

## Usage

1. Run the following commands from the app directory

   ```
   cd .docker
   docker compose build
   ```

2. Docker will install all requirements, create and apply migrations, and then start the server using the following commands from Dockerfile and docker-compose.yaml

   ```
   bash -c "python manage.py makemigrations
   && python manage.py migrate --run-syncdb
   && python manage.py runserver 0.0.0.0:8000"
   ```

3. Create a superuser account to access the Django admin panel (if needed):

   ```
   python manage.py createsuperuser
   ```

4. Access the application in your web browser at `http://localhost:8000/`.
