from django.forms import modelform_factory
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product
