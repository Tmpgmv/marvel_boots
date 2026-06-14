from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']  # обязательно для autocomplete_fields


admin.site.register(Product, ProductAdmin)