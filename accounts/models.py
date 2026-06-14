from django.db import models

# PREP {
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from orders.models import Order


class User(AbstractUser):
    patronymic = models.CharField(max_length=300,
                                  verbose_name="Отчество")

    def get_active_order(self):
        if self.is_client():
            order, _ = Order.objects.get_or_create(client=self,
                                                   status="Активный")
            return order
        else:
            raise ValueError("Только клиент может иметь активный заказ")

    def get_active_order_url(self):
        if self.is_client():
            order = self.get_active_order()
            return reverse_lazy("order", kwargs={'pk': order.pk})

    def get_full_name(self):
        return super().first_name + " " + self.patronymic + " " + super().last_name

    def is_admin(self):
        result = self.groups.filter(name='Администратор').exists() or self.is_superuser
        return result

    def is_manager(self):
        return self.groups.filter(name='Менеджер').exists()

    def is_client(self):
        return self.groups.filter(name__icontains='авторизированный').exists()

    def __str__(self):
        return self.get_full_name()

    def role(self):
        return self.groups.first() or ""

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

# } PREP
