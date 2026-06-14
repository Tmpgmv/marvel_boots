from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

from general.utils import choices


class Order(models.Model):
    STATUS_CHOICES = ["Активный", "Подтверждён", "Отменён", ]

    # PKGH Обновится при каждом изменении товара.
    # изменение - может быть одно - смена статуса товара.
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Дата/время заказа")
    client = models.ForeignKey("accounts.User",
                               on_delete=models.CASCADE,
                               verbose_name="Клиент")
    status = models.CharField(max_length=20,
                              choices=choices(STATUS_CHOICES),
                              default='Активный',
                              verbose_name="Статус")

    @admin.display(description='Итоговая сумма заказа', ordering='id')
    def get_total_sum(self):
        """PKGH Итоговая сумма заказа"""
        total_sum = 0
        for order_product in self.orderproduct_set.all():
            total_sum += order_product.amount * order_product.product.get_price_and_class().get("price")

        return f"{total_sum} руб."

    def __str__(self):
        return f"{self.created_at} - {self.client} - итого по заказу: {self.get_total_sum()}"


    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'



class OrderProduct(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name="Заказ")
    product = models.ForeignKey("products.Product",
                                on_delete=models.CASCADE,
                                verbose_name="Товар")
    size = models.ForeignKey("products.SizeEnabled",
                             on_delete=models.CASCADE,
                             verbose_name="Размер")
    amount = models.PositiveIntegerField(
        verbose_name="Количество")  # PKGH Очень важно, чтобы по умолчанию было значение. Потому что будем полагаться на get_or_create с выборкой не по количеству.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.order.client}: {self.product} - размер {self.size} - {self.amount} шт."

    def clean(self):
        if self.product != self.size.product:
            raise ValidationError("Размер надо выбирать только соответствюущий данному товару.")
        pass

    class Meta:
        ordering = ["-order__created_at", ]
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказах"
