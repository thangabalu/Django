from django import template
import re

register = template.Library()

@register.filter(name='extract_from_h_tag')

def extract_from_h_tag (value):
    match = re.search('<h>(.*)',value)
    if match:
        return match.group(1)
    
    
@register.filter(name='concatenate_two_strings_firstdiv')

def concatenate_two_strings_firstdiv (value):
    return "firsdiv_"+ str(value)

@register.filter(name='concatenate_two_strings_seconddiv')

def concatenate_two_strings_seconddiv (value):
    return "seconddiv_"+ str(value)