from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from orders.models import Order, OrderProduct
# from orders.forms import CartItemForm
# from orders.models import CartItem
from products.models import Product, SizeEnabled


# class CartCreateView(View):
#
#     def post(self, request, *args, **kwargs):
#         form = CartItemForm(request.POST)
#         if form.is_valid():
#             pass
#         else:
#             # Form is invalid - stay on product page with errors
#             product_id = request.POST.get('product_id')
#
#             if product_id:
#                 try:
#                     from products.models import Product
#                     product = Product.objects.get(pk=product_id)
#
#                     # Add error message
#                     messages.error(request, "Please fix the errors below.")
#
#                     # Render product detail page with form errors
#                     return render(request, 'products/product_detail.html', {
#                         'object': product,
#                         'form': form,  # Form with errors
#                     })
#                 except Product.DoesNotExist:
#                     messages.error(request, "Product not found.")
#                     return redirect('home')
#
#             messages.error(request, "Invalid form submission.")
#             return redirect('home')
#         return super().post(request, *args, **kwargs)


class OrderProductCreateView(
                             View):
    model = OrderProduct
    fields = '__all__'



    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        amount = self.request.POST.get('amount')
        size = self.request.POST.get('size')

        order = request.user.get_active_order()

        product = Product.objects.get(pk=product_id)

        try:
            self.validate_size(size)
            self.validate_amount(product_id, size, amount)

            order_product, created = OrderProduct.objects.get_or_create(
                order=order,
                product=product,
                size_id=size,
                defaults={'amount': amount,
                          "price": product.get_price_and_class().get("price")}
            )
            if not created:
                order_product.amount += int(amount)
                order_product.save()
            messages.success(request, "Товар добавлен к заказу.")
        except ValidationError as e:
            messages.error(request, e.message)

        return redirect(product.get_absolute_url())

    def validate_size(self, size):
        if not size:
            raise ValidationError("Нельзя заказать товар, не указав размер")

    def validate_amount(self, product_id, size, amount):
        # PKGH Проверяем только количество: размеры
        # пользователь выбирал из выпадающего списка - там уже нет неверных
        # размеров.

        try:
            amount = int(amount)
        except ValueError as e:
            raise ValidationError("Введите количество.")

        if amount < 0:
            raise ValidationError("Количество должно быть положительным числом.")

        stock = SizeEnabled.objects.get(pk=size).stock

        order = self.request.user.get_active_order()

        cart_items = order.orderproduct_set.filter(product_id=product_id, size=size).all()

        amount_in_cart = 0

        for cart_item in cart_items:
            amount_in_cart += cart_item.amount

        if (stock - int(amount) - amount_in_cart) < 0:
            msg = f"Доступно {stock} шт."
            if amount_in_cart > 0:
                msg += f" У вас в корзине {amount_in_cart} шт."

                available_amount = stock - amount_in_cart

                if available_amount == 0:
                    msg += " Вы не можете купить этот товар."
                else:
                    msg += f" Вы можете купить только {available_amount} шт."

            raise ValidationError(msg)


# class CartItemCreateView(SuccessMessageMixin,
#                          CreateView):
#     model = CartItem
#     fields = '__all__'
#     success_url = reverse_lazy("home")
#     success_message = "Товар добавлен в корзину"
#
#     def post(self, request, *args, **kwargs):
#         product_id = self.request.POST.get('product')
#         client = self.request.POST.get('client')
#         amount = self.request.POST.get('amount')
#         size = self.request.POST.get('size')
#
#         product = Product.objects.get(pk=product_id)
#
#         try:
#             self.validate_amount(product_id, size, amount)
#         except ValidationError as e:
#             messages.error(request, e.message)
#             return redirect(product.get_absolute_url())
#
#
#
#         CartItem.objects.create(product=product,
#                                 client_id=client,
#                                 size=size,
#                                 price=product.get_price_and_class().get("price"),
#                                 amount=amount,
#                                 )
#         messages.success(request, "Товра добавлен в корзину")
#         return redirect(product.get_absolute_url())
#
#     def validate_amount(self, product_id, size, amount):
#         # PKGH Проверяем только количество: размеры
#         # пользователь выбирал из выпадающего списка - там уже нет неверных
#         # размеров.
#         # Остальное - безопасно.
#         stock = SizeEnabled.objects.get(product_id=product_id,
#                                    size=size).stock
#
#         cart_items = CartItem.objects.filter(product_id=product_id, size=size).all()
#
#         amount_in_cart = 0
#
#         for cart_item in cart_items:
#             amount_in_cart += cart_item.amount
#
#         if (stock - int(amount) - amount_in_cart) < 0 :
#             raise ValidationError(f"Доступно {stock} шт., у вас в корзине {amount_in_cart} шт. Вы можете купить только {stock - amount_in_cart}")
#
#
#
#
#
class OrderDetailView(SuccessMessageMixin,
                      UpdateView):
    model = Order
    fields = ['status', ]
    success_message = "Статус заказа изменен"
    success_url = reverse_lazy('home')