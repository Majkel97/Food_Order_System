from django.contrib import admin

from orders.models import Order, OrderDetails, Menu, MenuType

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Menu)
admin.site.register(MenuType)
