from django import template
import re

register = template.Library()

@register.filter(name='extract_from_h_tag')

def extract_from_h_tag (value):
    match = re.search('<h>(.*)',value)
    if match:
        return match.group(1)