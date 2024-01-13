from django import template
from django.conf import settings

from cart.views import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def change_lang(context, lang: str, *args, **kwargs):
    path = context['request'].get_full_path()
    if path[1:3] in settings.LANG_LIST:
        path = path[4:]
    return f'/{lang}/{path}'


@register.simple_tag
def cart_len(request):
    return len(Cart(request))


@register.simple_tag
def cart_items(request):
    return Cart(request)
