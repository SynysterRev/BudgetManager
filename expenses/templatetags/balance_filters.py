from django import template

register = template.Library()


@register.filter(name='get_color')
def get_color(amount):
    try:
        amount = float(amount)
        return "text-alert" if amount < 0 else "text-success"
    except (ValueError, TypeError):
        return ""

@register.filter(name='get_abs')
def get_abs(amount):
    return abs(amount)
