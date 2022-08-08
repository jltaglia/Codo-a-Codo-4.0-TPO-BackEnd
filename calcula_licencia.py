from ast import match_case
import datetime as dt


DIA_ACT = int(dt.date.today().day)
MES_ACT = int(dt.date.today().month)
ANIO_ACT = int(dt.date.today().year)


def stod(fecha):
    '''
    Convierte una fecha en formato string a datetime
        fecha [str]: Fecha a convertrir
    '''
    if fecha == '':
        return None
    else:
        anio, mes, dia = fecha.split('-')
        return dt.date(int(anio), int(mes), int(dia))


def dias_d_lic(f_ing,f_ref):
    '''
    Calcula los días de licencia que corresponden
    por año según la antiguedad del empleado
        f_ing (date): Fecha de ingreso del empleado
        f_ref (date): Fecha de referencia desde donde
                     se calcula la licencia
    '''
    dt = (f_ref - f_ing).days + 1

    if dt < 1825:   # de 0 a 5 años - 1 dia
        return 14
    elif dt < 3650: # de 5 a 10 años - 1 dia
        return 21
    elif dt < 7300: # de 10 a 20 años - 1 dia
        return 28
    else:           #20 años o mas
        return 35



def calc_lic_en_curso(id_empleado, estado, *parametros):
    '''
    CALCULA LA LICENCIA DE UN EMPLEADO

    PARAMETROS:
           id_empleado: ID DEL EMPLEADO
                estado: 'alta' = al empleado se le está gestionando el alta en la empresa
                         'lic' = al empleado se le está calculando la licencia solicitada
            parametros: (fecha_ingreso, fecha_inicio, fecha_fin,
                          lic_en_curso, saldo_lic_en_curso, fecha_regreso, afecta_licencia)

                             fecha_ingreso - (str): fecha de ingreso a la empresa
                              fecha_inicio - (str): fecha de inicio de la licencia
                                 fecha_fin - (str): fecha fin de la licencia
                              lic_en_curso - (str): Año de la licencia en curso
                        saldo_lic_en_curso - (int): Saldo de la licencia en curso
                             fecha_regreso - (str): Fecha de regreso de la ultima licencia tomada
                          afecta_licencia - (bool): Si los días ingresados afectan
                                                      a licencia ordinaria en curso
    DEVUELVE:
          lic_en_curso - (int): Año de la licencia en curso del empleado
    saldo_lic_en_curso - (int): Saldo de la licencia en curso del empleado
             fecha_fin - (str): Fecha de finalizació de la licencia modificada dependiendo
                                de cual sea el día original de finalización
         fecha_regreso - (str): Fecha de regreso de la ultima licencia tomada por el empleado
              dias_lic - (int): Días de licencia ingresados y/o calculados
                pasado - (bool): Si se le otorgan licencias del siguiente año
    '''
    licen_curso = 0
    pasado = False
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
        fecha_ingreso = stod(parametros[0])
        fecha_inicio = stod(parametros[1])
        fecha_fin = stod(parametros[2])
        licen_curso = int(parametros[3])
        saldo_lic = int(parametros[4])
        fecha_regreso = stod(parametros[5])
        afecta_licencia = parametros[6]
        # CALCULA EL SIGUIENTE DIA A LA FECHA DE FINALIZACION DE LA LICENCIA
        # POR LAS DUDAS QUE SEA NO HABIL PARA SUMARLE LOS DIAS QUE HAGAN FALTA
        # HASTA EL PROXIMO HABIL
        sig_dia_alfin = fecha_fin + dt.timedelta(days=1)
        #
        if dt.datetime.weekday(sig_dia_alfin) == 6: # LICIENCIA COMIENZA EN DIA DOMINGO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
            fecha_fin = fecha_fin + dt.timedelta(days=1)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-12-25'): # NAVIDAD
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
            fecha_fin = fecha_fin + dt.timedelta(days=1)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-01-01'): # AÑO NUEVO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
            fecha_fin = fecha_fin + dt.timedelta(days=1)
        elif sig_dia_alfin == stod(str(ANIO_ACT) + '-05-01'): # DIA DEL TRABAJO
            fecha_regreso = fecha_fin + dt.timedelta(days=2)
            fecha_fin = fecha_fin + dt.timedelta(days=1)
        else:
            fecha_regreso = fecha_fin + dt.timedelta(days=1)

        # CALCULA EL NUMERO DE DIAS QUE HAY ENTRE LA FECHA DE INICIO Y
        # LA FECHA DE FINALIZACION DE LA LICENCIA, ES DECIR, EL NUMERO DE
        # DIAS DE LICENCIA QUE VA A GOZAR EL EMPLEADO.
        dias_lic = ((fecha_fin - fecha_inicio).days) + 1

        # SI AFECTA LA LICENCIA ORDINARIA EN CURSO
        # RECALCULA EL SALDO DE LA LICENCIA EN CURSO
        if afecta_licencia:
            saldo_lic = saldo_lic - dias_lic

            if saldo_lic <= 0: 
                # SE QUEDO SIN DIAS DE LA LICENCIA EN CURSO
                # SE LE ASIGNAN LOS DIAS DEL SIGUIENTE AÑO 
                # SEGUN LA ANTIGÜEDAD A ENERO DEL PROXIMO AÑO
                licen_curso += 1
                saldo_lic = dias_d_lic(fecha_ingreso, stod((str(licen_curso) + '-01-01'))) - abs(saldo_lic)
                pasado = True

    return licen_curso, saldo_lic, fecha_fin, fecha_regreso, dias_lic, pasado
