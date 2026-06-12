from django.contrib.postgres.search import SearchVector
from django.views.generic import TemplateView, ListView  # PREP

from orders.models import OrderProduct
from products.forms import SearchSortFilterForm
from products.models import SizeAvailable, Product


class HomeView(ListView):  # PREP
    """
    PREP
    Редактировать данный файл по необходимости.
    При подготовке заготовки проекта надо
    было вывести на экран какой-то шаблон.
    Реальная задача может сильно отличаться.
    """

    template_name = "home/home.html"  # PREP
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        form = SearchSortFilterForm(self.request.GET)
        context['form'] = form
        return context

    def get_queryset(self):
        sort = self.request.GET.get("sort", "more")
        search = self.request.GET.get("search", None)
        category = self.request.GET.get("filter", None)

        queryset = super().get_queryset()

        if sort == "more":
            queryset = queryset.order_by("-price")
        else:
            queryset = queryset.order_by("price")

        if category and category != "Все категории":
            queryset = queryset.filter(category=category)

        if search:
            queryset = (queryset.annotate(search=SearchVector(
                                                             'name',
                                                             'description',))
                                .filter(search__icontains=search))

        return queryset
