from django import template
import re

register = template.Library()

@register.filter(name='extract_from_h_tag')

def extract_from_h_tag (value):
    match = re.search('<h>(.*)',value)
    if match:
        return match.group(1)

@register.filter(name='extract_first_td')
    
def extract_first_td (value):
    return value[0]

@register.filter(name='extract_second_td')
    
def extract_first_td (value):
    return value[1]
    
@register.filter(name='concatenate_two_strings_firstdiv')

def concatenate_two_strings_firstdiv (value):
    return "firsdiv_"+ str(value)

@register.filter(name='concatenate_two_strings_seconddiv')

def concatenate_two_strings_seconddiv (value):
    return "seconddiv_"+ str(value)