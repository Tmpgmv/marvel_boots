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
    status = models.CharField(max_length=20, choices=choices(STATUS_CHOICES), default='Активный')

    def __str__(self):
        return f"{self.timestamp} - {self.client}"

    class Meta:
        ordering = ["-created_at"]


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name="Заказ")
    product = models.ForeignKey("products.Product",
                                on_delete=models.CASCADE,
                                verbose_name="Товар")
    size = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               verbose_name="Размер")
    amount = models.PositiveIntegerField(verbose_name="Количество") # PKGH Очень важно, чтобы по умолчанию было значение. Потому что будем полагаться на get_or_create с выборкой не по количеству.
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.order.client} - {self.product} - {self.size} - {self.amount}"

    def __str__(self):
        return f"{self.order} - {self.product} - {self.amount}"
