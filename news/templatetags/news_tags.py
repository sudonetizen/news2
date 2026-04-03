import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group):
    return user.groups.filter(name=group).exists()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

