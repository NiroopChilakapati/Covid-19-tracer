# Create a file called custom_filters.py in one of your app's folders, if it doesn't exist.
# Add the following code to custom_filters.py:

from django import template

register = template.Library()

@register.filter(name='remove_commas')
def remove_commas(value):
    return str(value).replace(',', '')
