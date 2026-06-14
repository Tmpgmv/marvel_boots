from django.contrib import admin

from orders.models import Order, OrderProduct


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 0
    autocomplete_fields = ['product', ]

class OrderAdmin(admin.ModelAdmin):
    exclude = []
    inlines = [OrderProductInline, ]
    list_display = ('id', 'client', 'created_at', 'status', 'get_total_sum', )

admin.site.register(Order, OrderAdmin)



class OrderProductAdmin(admin.ModelAdmin):
    model = OrderProduct
    exclude = []

admin.site.register(OrderProduct, OrderProductAdmin)