from django import template
from django.db.models.fields.files import ImageFieldFile

register = template.Library()


@register.filter
def get_fields(model):
    """
    Returns all non-relation fields of a model, checking detail_exclude attribute

    Применение:

    class Product(models.Model):
        exclude_from_detail = ['price']


    """
    # Проверяем атрибут класса detail_exclude
    exclude_fields = getattr(model.__class__, 'exclude_from_detail', [])

    fields = []
    for field in model._meta.get_fields():
        # Skip relationships and auto-created fields
        if field.one_to_many or field.many_to_many or field.auto_created:
            continue

        # Skip excluded fields
        if field.name in exclude_fields:
            continue

        value = getattr(model, field.name)
        fields.append({
            'label': field.verbose_name,
            'name': field.name,
            'value': value,
            'is_image': isinstance(value, ImageFieldFile),
        })
    return fields