from django import template

register = template.Library()


@register.filter(name='tdc')
def tdc(value: int):
    return '{:,}'.format(value)
