


def recalc_all_stock():
    """
    Полный пересчет всех остатков на складе.
    Пробегаем по всем подтвержденным заказам и пересчитываем.
    """
    from .models import  Order
    from products.models import SizeEnabled

    # Сначала восстанавливаем начальные остатки
    for size_item in SizeEnabled.objects.all():
        size_item.stock = size_item.initial_stock  # используем правильное имя поля
        size_item.save()

    # Потом проходим по всем ПОДТВЕРЖДЕННЫМ заказам и списываем
    for order in Order.objects.filter(status="Подтверждён"):
        for item in order.orderproduct_set.all():
            size_item = SizeEnabled.objects.get(
                product=item.product,
                size_av=item.size
            )
            size_item.stock -= item.amount
            size_item.save()