from django.template.library import Library

register = Library()


@register.filter(name="sorted")
def sorted_(thing):
    return sorted(thing)
