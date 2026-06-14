from django import forms

from orders.models import CartItem
from products.models import SizeEnabled
from general.utils import choices


class CartItemForm(forms.ModelForm):
    size = forms.ChoiceField(
        choices=[],
        label="Размер",
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial')
        if initial:
            product_id = initial.get('product')
        super().__init__(*args, **kwargs)

        # Populate size choices based on product

        sizes = SizeEnabled.objects.filter(
            product_id=product_id,
            stock__gt=0  # Only show sizes in stock
        )

        self.fields['size'].choices = choices(sizes)

        if not choices:
            self.fields['size'].choices = [('', 'Нет доступных размеров')]
            self.fields['size'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        exclude = []
        model = CartItem
        widgets = {
            'client': forms.HiddenInput(),
            'price': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }
