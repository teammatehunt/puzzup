from django import template

from puzzle_editing.models import User

register = template.Library()


@register.simple_tag
def avatar_list(users, linkify=False):
    """Displays a QuerySet of users"""

    return User.html_avatar_list_of(users.all(), linkify)
