from django import template

register = template.Library()


@register.filter
def modulo(num,pos):  # to extract the digits of the numbers(max 3 digit) 
    if pos == 0:
        return num%10
    elif pos == 1:
        return (num//10)%10
    return (num//100)%10 


