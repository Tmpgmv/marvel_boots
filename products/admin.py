from django.contrib import admin
from products.models import SizeEnabled, SizeAvailable
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']  # обязательно для autocomplete_fields


admin.site.register(Product, ProductAdmin)




# class SizeEnabledAdmin(admin.ModelAdmin):
#     model = SizeEnabled
#     list_display = ('product', 'size_av', 'stock')
#
#
#
# admin.site.register(SizeEnabled, SizeEnabledAdmin)