from django import forms

from general.utils import choices



class SearchSortFilterForm(forms.Form):

    CHOICES = [
        ('more', 'Больше'),
        ('less', 'Меньше'),
    ]

    sort = forms.ChoiceField(
        choices=CHOICES,
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


