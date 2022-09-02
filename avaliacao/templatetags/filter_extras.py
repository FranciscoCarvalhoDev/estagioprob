from django import template
register = template.Library()

@register.filter(name='define_conceitos')
def define_conceitos(value):
    value = float(value)

    if(value < 50):
        conceito = 'Insuficiente'
    elif(value < 65):
        conceito = 'Regular'
    elif(value < 86):
        conceito = 'Bom'
    elif(value >=86):
        conceito = 'Excelente'

    return conceito+' ( '+str(value)+' )'


register.filter('define_conceitos', define_conceitos)