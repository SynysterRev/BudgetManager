from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_classes(context, url_name):
    request = context['request']
    is_active = request.resolver_match.url_name == url_name
    base = ("font-medium w-full h-full flex px-6 py-3 "
            "text-center duration-150 transition-colors")
    if is_active:
        return (f"{base} bg-indigo-300/30 text-primary-indigo border-r-4 "
                f"border-primary-indigo")
    else:
        return f"{base} hover:bg-black/10"
