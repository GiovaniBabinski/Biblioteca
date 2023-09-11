from django import template
from datetime import date

register = template.Library()

@register.filter
def mostra_duracao(value1, value2):
    if all((isinstance(value1, date), isinstance(value2, date))):
        dias = (value1 - value2).days
        if dias == 1:
            return f"{dias} dia"
        else:
            return f"{dias} dias"
    return "Não devolvido"
