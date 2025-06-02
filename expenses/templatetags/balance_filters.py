from django import template

register = template.Library()


@register.filter(name='get_color')
def get_color(amount):
    try:
        amount = float(amount)
        return "text-alert" if amount < 0 else "text-success"
    except (ValueError, TypeError):
        return ""
