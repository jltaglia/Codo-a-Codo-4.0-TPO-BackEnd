from ast import match_case
import datetime as dt

from click import argument

DIA_ACT = int(dt.date.today().day)
MES_ACT = int(dt.date.today().month)
ANIO_ACT = int(dt.date.today().year)


def stod(fecha):
    '''
    Convierte una fecha en formato string a datetime
    '''
    if fecha == '':
        return None
    else:
        anio, mes, dia = fecha.split('-')
        return dt.date(int(anio), int(mes), int(dia))


def calc_lic_en_curso(id_empleado, estado, *fechas):
    '''
    CALCULA LA LICENCIA DE UN EMPLEADO

    PARAMETROS:
           id_empleado: ID DEL EMPLEADO
                estado: 'alta' = al empleado se le está gestionando el alta en la empresa
                         'lic' = al empleado se le está calculando la licencia solicitada
                fechas: (fecha_inicio, fecha_fin,
                          lic_en_curso, saldo_lic_en_curso, fecha_regreso, afecta_licencia)
                                - [str] fecha de inicio de la licencia
                                - [str] fecha fin de la licencia
                                - [str] Año de la licencia en curso
                                - [int] Saldo de la licencia en curso
                                - [str] Fecha de regreso de la ultima licencia tomada
                                - [bool] Si los días ingresados afectan
                                        a licencia ordinaria en curso
    DEVUELVE:
          lic_en_curso: Año de la licencia en curso del empleado (int)
    saldo_lic_en_curso: Saldo de la licencia en curso del empleado (int)
         fecha_regreso: Fecha de regreso de la ultima licencia tomada por el empleado (str)
              dias_lic: Días de licencia ingresados (int)

    '''
    licen_curso = 0
    if estado == 'alta':
        if MES_ACT > 7:
            licen_curso = ANIO_ACT + 1
        else:
            licen_curso = ANIO_ACT

        saldo_lic = 14
        dias_lic = 0
        fecha_regreso = dt.date.today()

    else:
        # Licencia a gozar desde el fecha_inicio hasta el fecha_fin
        # fecha_inicio
        fecha_inicio = stod(fechas[0])
        fecha_fin = stod(fechas[1])
        licen_curso = int(fechas[2])
        saldo_lic = int(fechas[3])
        fecha_regreso = stod(fechas[4])
        afecta_licencia = fechas[5]
        # CALCULA EL SIGUIENTE DIA A LA FECHA DE FINALIZACION DE LA LICENCIA
        # POR LAS DUDAS QUE SEA NO HABIL PARA SUMARLE LOS DIAS QUE HAGAN FALTA
        # HASTA EL PROXIMO HABIL
        sig_dia_alfin = dt.datetime.weekday(fecha_fin + 1)
        #
        if sig_dia_alfin == 1: # LICIENCIA COMIENZA EN DIA DOMINGO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-12-25'): # NAVIDAD
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-01-01'): # AÑO NUEVO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-05-01'): # DIA DEL TRABAJO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
        else:
            fecha_regreso = fecha_fin + dt.timedelta(days=1)

        # CALCULA EL NUMERO DE DIAS QUE HAY ENTRE LA FECHA DE INICIO Y LA FECHA DE FINALIZACION
        # DE LA LICENCIA
        dias_lic = (fecha_regreso - fecha_inicio).days




    return licen_curso, saldo_lic, fecha_regreso, dias_lic


# calc_lic_en_curso(1, 'norm', '11/07/2022', '21/07/2022')