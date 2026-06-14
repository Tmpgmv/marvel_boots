from django import forms
from django.core.validators import MinValueValidator

from general.utils import choices
from orders.models import OrderProduct
from products.models import SizeEnabled


class SearchSortFilterForm(forms.Form):

    CHOICES = ['Больше', 'Меньше',]

    sort = forms.ChoiceField(
        choices=choices(CHOICES),
        initial='more',
        required=False,
        label="Цена"
    )

    CATEGOGIES = ["Все категории", "Детская обувь", "Женская обувь", "Мужская обувь", ]

    filter = forms.ChoiceField(choices=choices(CATEGOGIES),
                                 required=False,
                                 label="Категория")


    search = forms.CharField(required=False,
                             label="Поиск")


# class OrderProductForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         # # PKGH Извлекаем product_id из kwargs ДО вызова super()
#         # # Причина - super() не ожидает этот аргумент.
#         # self.product_id = kwargs.pop('product_id', None)
#
#         super().__init__(*args, **kwargs)
#         if (kwargs.get("initial")):
#             sizes = SizeEnabled.objects.filter(
#                 product__pk=kwargs.get("initial").get("product_id"),
#                 stock__gt=0
#             ).all()
#
#             self.fields['size'].choices = choices(sizes)
#
#             self.fields['product_id'].initial = kwargs.get("initial").get("product_id")
#
#     size = forms.ChoiceField(
#         choices=[],
#         label="Размер",
#     )
#
#     amount = forms.IntegerField(
#         label="Количество",
#     )
#
#     product_id = forms.IntegerField(widget=forms.HiddenInput())
#
#     def clean_size(self):
#         data = self.cleaned_data["size"]
#         return data
#
#     def clean_amount(self):
#         data = self.cleaned_data["amount"]
#         size_enabled = SizeEnabled.objects.get(pk=self.data.get("product_id"))
#         if data < size_enabled.stock:
#             raise forms.ValidationError("Количество меньше имеющегося")
#
#         return data
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         pass



# class CartForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if (kwargs.get("initial")):
#             sizes = SizeEnabled.objects.filter(
#                 product__pk=kwargs.get("initial").get("product_id"),
#                 stock__gt=0
#             ).all()
#
#             self.fields['size'].choices = choices(sizes)
#
#             self.fields['product_id'].initial = kwargs.get("initial").get("product_id")
#
#     size = forms.ChoiceField(
#         choices=[],
#         label="Размер",
#     )
#
#     amount = forms.IntegerField(
#         label="Количество",
#     )
#
#     product_id = forms.IntegerField(widget=forms.HiddenInput())
#
#     client = forms.IntegerField(widget=forms.HiddenInput())
#
#     def clean_size(self):
#         data = self.cleaned_data["size"]
#         return data
#
#     def clean_amount(self):
#         data = self.cleaned_data["amount"]
#         size_enabled = SizeEnabled.objects.get(pk=self.data.get("product_id"))
#         if data < size_enabled.stock:
#             raise forms.ValidationError("Количество меньше имеющегося")
#
#         return data
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         pass


