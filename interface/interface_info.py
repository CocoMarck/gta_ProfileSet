from logic.Modulo_System import *
from data.gta_modloader_function import *
import os


display = get_display_resolution()

def get_display_number(multipler=0, divisor=0, based='width'):
    if based == 'width':
        base = display[0]
    else:
        base = display[1]

    lim_max = int( max(display)*0.75 )
    lim_min = 8

    number = None
    if multipler > 0:
        number = base*multipler
    else:
        if divisor > 0:
            number = base/divisor

    if not number == None:
        if number > lim_max:
            return lim_max
        elif number < lim_min:
            return lim_min
        else:
            return int(number)

# Establecer dimenciones de windegts y ventana
# Limite de resolucion: Anchura y altura de 480px como minimo.
num_font = get_display_number(divisor=120)
num_space_padding = int(num_font/3)

nums_win_main = [
    get_display_number(multipler=0.3, based='width'),
    get_display_number(multipler=0.3, based='height')
]
nums_win_set_something = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.35, based='height')
]
nums_win_cfg_param = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.25, based='height')
]

'''
print(display)
print(num_font)
print(num_space_padding)
print(nums_win_main)
print(nums_win_set_something)
print(nums_win_cfg_param)
'''

# Fuente de texto
if get_system() == 'win':
    #font = 'Cascadia Code'
    font = 'Consolas'
    #font = 'times'
else:
    font = 'Liberation Mono'


# Icono
icon_gta_ProfileSet = os.path.join(dir_main, 'resources', 'gta_ProfileSet.ico')
