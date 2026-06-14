from datetime import datetime
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse_lazy

from general.utils import choices
from orders.models import Order


class Product(models.Model):
    exclude_from_detail = ['price']

    CATEGOGIES = ["Детская обувь", "Женская обувь", "Мужская обувь", ]
    SUBCATEGORIES = ["Босоножки", "Ботинки", "Кроссовки", "Сапоги", "Туфли", ]

    category = models.CharField(max_length=100,
                                choices=choices(CATEGOGIES),
                                null=False, blank=False,
                                verbose_name="Категория")

    subcategory = models.CharField(max_length=100,
                                   choices=choices(SUBCATEGORIES),
                                   null=False, blank=False,
                                   verbose_name="Подкатегория")

    photo = models.ImageField(verbose_name="Изображение",
                              default="picture.png")
    name = models.CharField(max_length=100,
                            verbose_name="Наименование товара")
    manufacturer = models.CharField(max_length=100,
                                    verbose_name="Производство")
    description = models.TextField(verbose_name="Описание")

    ingredients = models.CharField(max_length=1000, verbose_name="Состав")

    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.00'))],
                                verbose_name="Цена")

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"pk": self.pk})

    def get_amount(self):
        """
        PKGH
        Отобразить для количества: «много», если более пяти единиц товарных позиций и «мало»,
        если менее или равно пяти.

        :return: "Мнгого" | "Мало"
        """

        amount = SizeEnabled.objects.filter(product=self).count()
        return "Много" if amount > 5 else "Мало"

    def too_few(self):
        """
        В списке товаров необходимо подсвечивать светло-красным цветом
        товары, доступное для заказа количество которых меньше или равно трем.

        pink - это класс для HTML-тега.

        :return: "pink" | ""
        """
        amount = SizeEnabled.objects.filter(product=self).count()
        return "pink" if amount <= 3 else ""

    def get_price_and_class(self):
        """
        PKGH

        Рядом с ценой в шаблоне выведен бейдж "Скидка".
        И применяется класс, возвращаемый из этого метода.

        По умолчанию - возвращаем d-none (скрыть).
        Если применяем скидку, не передаем d-none.

        :return: Примеры: (100, "d-none"), (100, "")
        """
        start_date = datetime(2026, 4, 1, 0, 0, 0)
        end_date = datetime(2026, 4, 30, 23, 59, 59)
        number_of_orders_in_april = Order.objects.filter(
            orderproduct__product=self,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).distinct().count()

        result = {"price": self.price, "class": "d-none"}

        if number_of_orders_in_april == 0:
            result["price"] = self.price * (100 - 25) / 100
            result["class"] = ""

        return result

    def get_absolute_url(self):
        return reverse_lazy("product-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'subcategory', 'name']



class SizeAvailable(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Размер")

    def __str__(self):
        return str(self.size)

    class Meta:
        ordering = ['product', 'size']


class SizeEnabled(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Размер")
    stock = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return str(self.size)

    class Meta:
        ordering = ['product', 'size']

