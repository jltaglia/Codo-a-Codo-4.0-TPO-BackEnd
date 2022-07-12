"""
MODULO DE RRHH
"""
import os
import rrhhAdmLicencias as lc
import rrhhAdmPersonal as ap
import rrhhNovedades as nv

def clear_console():
    """
    PARA LIMPIAR LA PANTALLA DE LA CONSOLA
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
#
# COMIENZO RECURSOS HUMANOS
#
# 1
#
while True:
    clear_console()
    print(' 1. Administ. de Personal     ')
    print(' 2. Administ. de Licencias    ')
    print(' 3. Novedades                 ')
    elec2 = input('Ingrese su opción: ')

    match elec2:

        case '0':
            clear_console()
            break

        case '1':
            clear_console()
            print('1. Adm. Personal')
            print('----------------')
            print('1. Modificar  ')
            print('2. Bajas      ')
            print('3. Altas      ')
            print('4. Listados   ')
            while True:
                elec3 = input('1. > ')
                if elec3 == '0':
                    break
                ap()
                # abmlPers(elec3)

        case '2':
            clear_console()
            print('2. Admin de Licencias')
            print('---------------------')
            print('1.Ingreso Licencia ')
            print('2.Consulta Licencia')
            print('3.Lista de Saldos  ')
            print('4.Resumen Licencias')
            while True:
                elec3 = input('2. > ')
                if elec3 == '0':
                    break
                lc()
                # licencias(elec3)

        case '3':
            clear_console()
            print('3. Novedades          ')
            print('----------------------')
            print('1. Ingreso de Novedad ')
            print('2. Información Mensual')
            while True:
                elec3 = input('3. > ')
                if elec3 == '0':
                    break

                nv()
                # rhNoved(elec3)

#
#
# FIN CICLO PRINCIPAL
#
# FIN BLOQUE PRINCIPAL DEL PROGRAMA
#
#
#
# FIN RECURSOS HUMANOS
#
#
