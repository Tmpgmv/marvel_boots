from django import template
from django.db.models.fields.files import ImageFieldFile

register = template.Library()


@register.filter
def get_fields(model):
    """Returns all non-relation fields of a model"""
    fields = []
    for field in model._meta.get_fields():
        # Skip relationships and auto-created fields
        if field.one_to_many or field.many_to_many or field.auto_created:
            continue

        value = getattr(model, field.name)
        fields.append({
            'label': field.verbose_name,
            'name': field.name,
            'value': value,
            'is_image': isinstance(value, ImageFieldFile),
        })
    return fields