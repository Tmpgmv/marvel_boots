from django.db import models


class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True,
                                verbose_name="Дата/время заказа")
    client = models.ForeignKey("accounts.User",
                               on_delete=models.CASCADE,
                               verbose_name="Клиент")

    def __str__(self):
        return f"{self.timestamp} - {self.client}"

    class Meta:
        ordering = ["-timestamp"]

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
    amount = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.order} - {self.product} - {self.amount}"



class CartItem(models.Model):



    client = models.ForeignKey("accounts.User",
                               on_delete=models.CASCADE,
                               verbose_name="Клиент")
    product = models.ForeignKey("products.Product",
                                on_delete=models.CASCADE,
                                verbose_name="Товар")
    size = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               verbose_name="Размер")
    amount = models.PositiveIntegerField(verbose_name="Количество")

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name="Цена")

    def __str__(self):
        return f"{self.order} - {self.product} - {self.amount}"

    class Meta:
        ordering = ["-product", "price", ]
