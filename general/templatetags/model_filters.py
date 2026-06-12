from django import template
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from django.forms import model_to_dict

register = template.Library()

@register.filter
def is_image_field(value):
    """Check if value is an ImageFieldFile"""
    return isinstance(value, ImageFieldFile)

@register.filter
def is_url_field(value):
    """Check if value looks like a URL"""
    if isinstance(value, str):
        return value.startswith(('http://', 'https://', '/'))
    return False

@register.filter
def is_list(value):
    """Check if value is a list, tuple, or queryset"""
    return isinstance(value, (list, tuple, QuerySet))