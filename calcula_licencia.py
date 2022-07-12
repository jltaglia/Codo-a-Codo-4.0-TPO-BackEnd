import datetime as dt

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
        dia, mes, anio = fecha.split('/')
        return dt.date(int(anio), int(mes), int(dia))



def calc_lic_en_curso(id_empleado, estado, *fechas):
    '''
    CALCULA LA LICENCIA DE UN EMPLEADO

    ID_EMPLEADO: ID DEL EMPLEADO
    ESTADO: 'alta' = al empleado se le está gestionando el alta en la empresa
            'norm' = al empleado se le está calculando la licencia solicitada
    '''
    licen_curso = 0
    if estado == 'alta':
        if MES_ACT > 7:
            licen_curso = ANIO_ACT + 1
        else:
            licen_curso = ANIO_ACT
    
        saldo_lic = 14

    else:
        saldo_lic = 0
        licen_curso = 0


        finie, ffine = fechas
        print(DIA_ACT, MES_ACT, ANIO_ACT)
        print(finie, ffine)


        fecha1 = dt.datetime.strptime('01 06 2005', '%d %m %Y').date() 
        fecha2 = dt.date(2005, 6, 1)
        fecha3 = stod(finie)

        print(fecha1, fecha2, fecha3)

        date_1 = dt.datetime.strptime(finie, "%d/%m/%Y")
        end_date = date_1 + dt.timedelta(days=10)

        print(end_date.date())



            # @ 8,4 say "Licencia a gozar desde el          hasta el "
			# 	@ 8,30 get finie
			# 	@ 8,48 get ffine valid ffine >= finie
        # if w(ffine + 1) = 1 # LICIENCIA COMIENZA EN DIA DOMINGO
    # 			ddreg := ffine + 2
            
    # 		case (ffine + 1) = ctod("25/12/" + str(year(ffine),4)) // NAVIDAD
    # 			ddreg := ffine + 2
            
    # 		case (ffine + 1) = ctod("01/01/" + str(year(ffine),4)) // A�O NUEVO
    # 			ddreg := ffine + 2
            
    # 		case (ffine + 1) = ctod("01/05/" + str(year(ffine),4)) // DIA DEL TRABAJO
    # 			ddreg := ffine + 2
            
    # 		otherwise
    # 			ddreg := ffine + 1
    # 	endcase
			# 	@ 10,4 say "Fecha estimada de regreso :" get ddreg valid ddreg > ffine
			# 	@ 12,4 say "La licencia ingresada..."
			# 	@ 13,4 say "� Afecta a las vacaciones disponibles ? [SI=Y / NO=N]" get afecta picture "Y"
			# 	set cursor on
			# 	read
			# 	set cursor off
			# 	son := alert ("� Confirma los datos ingresados ?", {" SI "," NO "})
			# 	if son = 2
			# 		loop // 1
			# 	endif
			# 	//
			# 	// ACTUALIZACION DE ARCHIVOS DE EMPLEADOS
			# 	//
			# 	archivo := "LEG_" + padl(alltrim(str(vcemp)),3,"0")
			# 	archivoc := dirb6 + archivo + ".dbf"
			# 	//
			# 	use (archivoc);
			# 		index (dirb6 + archivo + ".ntx");
			# 		alias em new
			# 	select em
			# 	em -> (dbappend())
			# 	replace em -> desde with finie
			# 	replace em -> hasta with ffine
			# 	replace em -> motivo with evento
			# 	replace em -> cantidad with (ffine - finie) + 1
			# 	select ps
			# 	replace ps -> fe_regreso with ddreg
			# 	if afecta
			# 	//
			# 	// SI LA LICENCIA INGRESADA AFECTA
			# 	// AL SALDO ACTUAL DE DIAS DE VACACIONES
			# 	//
			# 		nvo_saldo := ps -> saldo_lic - em -> cantidad
			# 		if nvo_saldo < 0
			# 			resto := abs(nvo_saldo)
			# 			vie_licc := ctod(;
			# 					str(day(ps -> f_ing))+ "/" +;
			# 					str(month(ps -> f_ing))+ "/" +;
			# 					str(ps -> lic_curso);
			# 					)
						
			# 			vie_dlic := dias_d_lic(ps -> f_ing , vie_licc)
			# 			vlic_curso := ctod(;
			# 					str(day(ps -> f_ing))+ "/" +;
			# 					str(month(ps -> f_ing))+ "/" +;
			# 					str(ps -> lic_curso + 1);
			# 					)
			# 			// 
			# 			// CALCULO DE LOS DIAS DE LICENCIA
			# 			//
			# 			dias_lic := dias_d_lic(ps -> f_ing , vlic_curso)
			# 			//
			# 			//
			# 			//
			# 			replace ps -> saldo_lic with (dias_lic - resto)
			# 			replace ps -> lic_curso with year(vlic_curso)
			# 		else
			# 			if nvo_saldo <> 0
			# 				vlic_curso := ctod(;
			# 					str(day(ps -> f_ing))+ "/" +;
			# 					str(month(ps -> f_ing))+ "/" +;
			# 					str(ps -> lic_curso))
			# 			else
			# 				vie_licc := ctod(;
			# 						str(day(ps -> f_ing))+ "/" +;
			# 						str(month(ps -> f_ing))+ "/" +;
			# 						str(ps -> lic_curso);
			# 						)
			# 				vie_dlic := dias_d_lic(ps -> f_ing , vie_licc)
			# 				vlic_curso := ctod(;
			# 					str(day(ps -> f_ing))+ "/" +;
			# 					str(month(ps -> f_ing))+ "/" +;
			# 					str(ps -> lic_curso + 1);
			# 					)
			# 			endif
			# 			// 
			# 			// CALCULO DE LOS DIAS DE LICENCIA
			# 			//
			# 			dias_lic := dias_d_lic(ps -> f_ing , vlic_curso)
			# 			//
			# 			//
			# 			//
			# 			if nvo_saldo = 0
			# 				replace ps -> lic_curso with ps -> lic_curso + 1
			# 				replace ps -> saldo_lic with dias_lic
			# 			else
			# 				diasytom := dias_lic - ps -> saldo_lic
			# 				replace ps -> lic_curso with year(vlic_curso)
			# 				replace ps -> saldo_lic with nvo_saldo
			# 			endif
			# 		endif
			# 	endif






    return licen_curso, saldo_lic


calc_lic_en_curso(1, 'norm', '11/07/2022', '21/07/2022')