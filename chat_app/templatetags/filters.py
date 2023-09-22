from django import template

register = template.Library()

@register.filter
def clean_response(response):
    if isinstance(response, list):

        cleaned_response = ' '.join([item.replace('System: ', '') for item in response])


        cleaned_response = cleaned_response.replace('\n\n', '\n')

        return cleaned_response
    elif isinstance(response, str):
        return response.replace('System: ', '').replace('\n\n', '\n')
    return response