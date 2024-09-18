from django import template
from django.forms import BoundField

register = template.Library()


@register.filter(name='addclass')
def addclass(field, css):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css})
    elif isinstance(field, str):
        return field
    else:
        raise ValueError("Expected a form field or string")