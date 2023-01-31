from django import template

register = template.Library()


@register.filter()
def name_list(users):
    """Displays a comma-delimited list of users"""
    return ", ".join([str(user) for user in users])


@register.filter()
def display_name(user):
    """Shows a user's display name (default to credits if not set)."""
    if not user:
        return "none"

    return str(user)
