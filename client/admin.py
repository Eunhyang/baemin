from django.contrib import admin
from .models import Client, Order, Ordertime
# Register your models here.
@admin.register(Client, Order, Ordertime)
class ClientAdmin(admin.ModelAdmin):
    pass
