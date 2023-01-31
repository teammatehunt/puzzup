from django import template

register = template.Library()


@register.inclusion_tag("tags/answer.html")
def formatted_answer(answer):
    """Displays a formatted version of the answer"""
    return {
        "answer": answer,
    }
