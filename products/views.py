from django.forms import modelform_factory
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # Create a form from the model (readonly)
    #     form_class = modelform_factory(self.model, fields='__all__')
    #     form = form_class(instance=self.object)
    #
    #     context['form'] = form
    #     context['verbose_name'] = self.model._meta.verbose_name
    #
    #     return context