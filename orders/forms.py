from decimal import Decimal

from django import forms

from general.utils import choices
from products.models import SizeEnabled

class OrderProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        size_enabled = SizeEnabled.objects.filter(product__pk=kwargs["initial"]['product_id'],
                                                  stock__gt=0 ).all()

        self.fields["size"].queryset = size_enabled



    product_id = forms.CharField(
        widget=forms.HiddenInput(),
    )

    size = forms.ModelChoiceField(
        queryset=None,
        label="Размер",
    )

    amount = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Цена"
    )

