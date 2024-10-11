from django.contrib import admin

from order.models import Order, Ticket


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass