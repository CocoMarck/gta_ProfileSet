import argparse
from data.gta_modloader_function import *


# Objeto para los parametros
parser = argparse.ArgumentParser()

parser.add_argument(
    '-sp',
    '--set_profile',
    help='Select a profile'
)

parser.add_argument(
    '-cp',
    '--current_profile',
    help='Get the current selected profile',
    action='store_true'
)

parser.add_argument(
    '-gp',
    '--get_profiles',
    help='Get all profiles',
    action='store_true'
)

parser.add_argument(
    '-ne',
    '--no_execute',
    help='Do not run the game',
    action='store_true'
)

# Obtener argumentos dados por el usuario
args = parser.parse_args()




# Establecer opciones seleccionadas
print('Test to pass:')
if test_to_pass() == True:
    print('Pass...\n\n')

    #print(
    #    args.set_profile,
    #    args.current_profile,
    #    args.get_profiles,
    #    args.no_execute
    #)

    if not args.set_profile == None:
        go = False
        for profile in get_profiles():
            if profile == args.set_profile:
                go = True
        if go == True:
            set_profile( profile=args.set_profile )
            print(f'Selected profile: {args.set_profile}')
        else:
            print(f'ERROR "{args.set_profile}" is not a profile')

    if args.current_profile == True:
        print( f'Current profile: {get_current_profile()}' )

    if args.get_profiles == True:
        print('Profiles:')
        for profile in get_profiles():
            print(profile)
        print()

    if args.no_execute == False:
        print('Execute the game...')
        execute_game()
