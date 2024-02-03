
from django.contrib import admin
from .models import Product, AdvUser, Order

admin.site.register(AdvUser)
admin.site.register(Product)
admin.site.register(Order)
