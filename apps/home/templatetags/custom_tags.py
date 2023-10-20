# Django's Libraries
import os
from django import template


register = template.Library()

@register.inclusion_tag('menu.html',
    takes_context=False)
def tag_menu(_user):

    contexto = {
        'user': _user,
    }
    return contexto