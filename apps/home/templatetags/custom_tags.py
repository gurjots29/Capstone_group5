# Django's Libraries
import os
from django import template
from apps.users.models import Volunteer

register = template.Library()

@register.inclusion_tag('menu.html',
    takes_context=False)
def tag_menu(_user):

    contexto = {
        'user': _user,
    }
    return contexto


@register.simple_tag(takes_context=True)
def get_volunteer_id(context):
    request = context['request']
    if request.user.is_authenticated:
        try:
            volunteer = Volunteer.objects.get(user=request.user)
            return volunteer.id
        except Volunteer.DoesNotExist:
            return None
    return None