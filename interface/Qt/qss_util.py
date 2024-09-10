text_list_widget = [
    'Label',
    'ComboBox',
    'LineEdit',
]
number = 0
for x in text_list_widget:
    text_list_widget[number] = f'Q{x}'
    number += 1


# Estilo de programa
def text_widget_style( widget=None, font=None, font_size=None, margin=None, padding=None, idented=0 ):
    text = ''

    # Establecer si se pondran corchetes o no {}
    # Inicio de corchete (solo si shell esta en true)
    shell = False
    if type(widget) == str:
        shell = True
        text += widget
        text += ' {\n'

    # Establecer el espacio de indentado
    space = ''
    if idented > 0:
        for x in range(0, idented):
            space += ' '


    # Agregar o no parametros
    if type(font) == str:
        text += f'{space}font-family: {font};\n'

    if type(font_size) == int:
        text += f'{space}font-size: {font_size}px;\n'

    if type(margin) == int:
        margin_xy = [int(margin/2), int(margin/4)]
        text += (
            f'{space}margin-left: {margin_xy[0]}px;\n'
            f'{space}margin-right: {margin_xy[0]}px;\n'
            f'{space}margin-top: {margin_xy[1]}px;\n'
            f'{space}margin-bottom: {margin_xy[1]}px;\n'
        )

    if type(padding) == int:
        text += f'{space}padding: {padding}px;\n' # Size adicional para el widget


    # Cierre de corchete
    if shell == True:
        text += '}\n'


    # Devolver texto
    return text
