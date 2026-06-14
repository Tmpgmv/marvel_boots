from django.forms import modelform_factory
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, CreateView

from orders.models import OrderProduct
from orders.forms import CartItemForm
from products.models import Product, SizeEnabled


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = CartItemForm(initial={"product": self.object.pk,
                                     "client": self.request.user.pk,
                                     "price": self.object.get_price_and_class(), })
        context['form'] = form

        # PKGH Добавляем доступные размеры для отображения

        return context
