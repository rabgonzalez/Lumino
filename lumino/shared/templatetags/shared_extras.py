from django import template
from django.utils.translation import get_language

register = template.Library()


@register.inclusion_tag('includes/setlang.html')
def setlang():
    LANGUAGES = ('en', 'es')
    current_language = get_language()
    return {'languages': LANGUAGES, 'current_language': current_language}
