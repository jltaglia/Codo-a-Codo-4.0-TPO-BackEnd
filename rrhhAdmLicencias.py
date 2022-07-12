#include "inkey.ch"
#
#
#
def licencias(elec3):
	#
	private evento,finie,ffine,nvo_saldo,archivo,archivoc,resto,j
	private dias_lic,vlic_curso,ddreg,vie_dlicc,vie_licc,diasytom
	#
	vcemp = 0
	j = 1
	i = 0
	sepa = False
	afecta = False
	cdv6 = 0
	evento = 0
	finie = ctod("  /  /  ")
	ffine = ctod("  /  /  ")
	ddreg = ctod("  /  /  ")
	nvo_saldo = 0
	resto = 0
	dias_lic = 0
	vlic_curso = ctod("  /  /  ")
	imp_fa = space(4)
	vie_licc = 0
	vie_dlic = 0
	diasytom = 0
	pimp = "P"
	finr = ffir = ctod("  /  /  ")
	#
	use (dirb6+"personal") index (dirb6+"persona1"),(dirb6+"persona2"),(dirb6+"persona3") alias ps new
	use (dirb6+"categori") alias ct new
	use (dirb6+"est_civ") alias ec new
	use (dirb6+"tipo_doc") alias td new
	use (dirb6+"eventos") alias ev new
	#
	restore from impresos.mem additive
	#
	match elec3:
		case '1':
			while True: # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,16,78," 5.2. CONFECCION PLANILLA DE LICENCIA ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@ 9,2  say "���������������������������������������������������������������������������ĺ"
				#
				@ 4,4 say "C�digo de Empleado :" get vcemp picture "999"
				set cursor on
				read
				set cursor off
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return

				ps -> (dbgotop())
				ps -> (dbseek(vcemp))
				if ps -> (found()):
					#
					while True: # 2
					#
						@ 4,30 say alltrim(ps -> apellido) + ", " + alltrim(ps -> nombres)
						@ 6,4  say "C�digo de Licencia :" get evento picture "99";
							valid left(str(evento,2),1) = "1"
						set cursor on
						read
						set cursor off
						if lastkey() == K_ESC:
							restscreen(0,0,23,79,sc)
							close all
							return

						select ev
						ev -> (dbgotop())
						locate for ev -> cd_evento = evento
						if ev -> (found()):
							@ 6,32 say ev -> desc
						else:
							tone(100,3)
							alert ("C�digo de Licencia inexistente...")
							loop # 2

						exit # 2
					#
					# 2
					#
					@ 8,4 say "Licencia a gozar desde el          hasta el "
					@ 8,30 get finie
					@ 8,48 get ffine valid ffine >= finie
					set cursor on
					read
					set cursor off
					if lastkey() == K_ESC:
						restscreen(0,0,23,79,sc)
						close all
						return

					@ 8,58 say "** " + alltrim(str((ffine - finie) + 1)) + " dias de lic.**"
					match :
						case dow(ffine + 1) = 1 # DOMINGO
							ddreg = ffine + 2
						
						case (ffine + 1) = ctod("25/12/" + str(year(ffine),4)) # NAVIDAD
							ddreg = ffine + 2
						
						case (ffine + 1) = ctod("01/01/" + str(year(ffine),4)) # A�O NUEVO
							ddreg = ffine + 2
						
						case (ffine + 1) = ctod("01/05/" + str(year(ffine),4)) # DIA DEL TRABAJO
							ddreg = ffine + 2
						
						case _:
							ddreg = ffine + 1

					@ 10,4 say "Fecha estimada de regreso :" get ddreg valid ddreg > ffine
					@ 12,4 say "La licencia ingresada..."
					@ 13,4 say "� Afecta a las vacaciones disponibles ? [SI=Y / NO=N]" get afecta picture "Y"
					set cursor on
					read
					set cursor off
					son = alert ("� Confirma los datos ingresados ?", {" SI "," NO "})
					if son == 2:
						loop # 1

					#
					# ACTUALIZACION DE ARCHIVOS DE EMPLEADOS
					#
					archivo = "LEG_" + padl(alltrim(str(vcemp)),3,"0")
					archivoc = dirb6 + archivo + ".dbf"
					#
					use (archivoc) index (dirb6 + archivo + ".ntx") alias em new
					select em
					em -> (dbappend())
					replace em -> desde with finie
					replace em -> hasta with ffine
					replace em -> motivo with evento
					replace em -> cantidad with (ffine - finie) + 1
					select ps
					replace ps -> fe_regreso with ddreg
					if afecta:
						#
						# SI LA LICENCIA INGRESADA AFECTA
						# AL SALDO ACTUAL DE DIAS DE VACACIONES
						#
						nvo_saldo = ps -> saldo_lic - em -> cantidad
						if nvo_saldo < 0:
							resto = abs(nvo_saldo)
							vie_licc = ctod(
									str(day(ps -> f_ing))+ "/" +
									str(month(ps -> f_ing))+ "/" +
									str(ps -> lic_curso)
									)
							
							vie_dlic = dias_d_lic(ps -> f_ing , vie_licc)
							vlic_curso = ctod(
									str(day(ps -> f_ing))+ "/" +
									str(month(ps -> f_ing))+ "/" +
									str(ps -> lic_curso + 1)
									)
							# 
							# CALCULO DE LOS DIAS DE LICENCIA
							#
							dias_lic = dias_d_lic(ps -> f_ing , vlic_curso)
							#
							#
							#
							replace ps -> saldo_lic with (dias_lic - resto)
							replace ps -> lic_curso with year(vlic_curso)
						else:
							if nvo_saldo != 0:
								vlic_curso = ctod(
									str(day(ps -> f_ing))+ "/" +
									str(month(ps -> f_ing))+ "/" +
									str(ps -> lic_curso)
									)
							else:
								vie_licc = ctod(
										str(day(ps -> f_ing))+ "/" +
										str(month(ps -> f_ing))+ "/" +
										str(ps -> lic_curso)
										)
								vie_dlic = dias_d_lic(ps -> f_ing , vie_licc)
								vlic_curso = ctod(
									str(day(ps -> f_ing))+ "/" +
									str(month(ps -> f_ing))+ "/" +
									str(ps -> lic_curso + 1)
									)
							# 
							# CALCULO DE LOS DIAS DE LICENCIA
							#
							dias_lic = dias_d_lic(ps -> f_ing , vlic_curso)
							#
							#
							#
							if nvo_saldo == 0:
								replace ps -> lic_curso with ps -> lic_curso + 1
								replace ps -> saldo_lic with dias_lic
							else:
								diasytom = dias_lic - ps -> saldo_lic
								replace ps -> lic_curso with year(vlic_curso)
								replace ps -> saldo_lic with nvo_saldo

					son = alert ("�Imprime la planilla correspondiente?", {" SI "," NO "})
					if son == 1:
						#
						# RUTINA PARA IMPRIMIR
						# LA PLANILLA DE LICENCIA
						#
						set console off
						set printer on
						set printer to (imp_fb)
						#
						for i in range(1,3):
							? "EL FIDEO FELIZ"
							?? " de Jose F. Pes"
							? "Perito Moreno 276, Rawson.(CH) - Tel/Fax (0280) 448-2993 448-5516"
							? "fideofelizrw@gmail.com"
							? "��������������������������������������������������������������������������������"
							?;?
							? space(10) + "PLANILLA DE LICENCIA"
							?? space(10) + "( " + ev -> desc + " )"
							? space(10) + "��������������������"
							?;?
							if i == 1:
								if dow(date() - 1) == 1:
									? space(50) + "Rawson, Chubut " + dtoc(date() - 3)
								else:
									? space(50) + "Rawson, Chubut " + dtoc(date() - 1)
							else:
								? space(50) + "Rawson, Chubut " + dtoc(date())

							?
							?
							if i == 1:
								? "Por intermedio de la presente le solicito a Usted que mi pr�ximo goce"
								? "vacacional "
							else:
								? "Por intermedio de la presente le comunicamos a Ud. que el goce vacacional"
								? "solicitado, correspondiente al a�o "

							if i == 2:
								match
									case nvo_saldo = 0
										?? alltrim(str((year(vlic_curso) - 1)))
									
									case nvo_saldo > 0
										?? str(year(vlic_curso))
										
									case nvo_saldo < 0
										?? alltrim(str((year(vlic_curso) - 1))) + " / " + str(year(vlic_curso))
									

							if i == 1:
								?? "me sea otorgado a partir del d�a " + dtoc(finie)
							else:
								?? ", le ha sido otorgado a partir"
								? "del dia " + dtoc(finie)

							?? " y hasta el d�a " 
							?? dtoc(ffine) 
							if i == 1:
								? "asumiendo la responsabilidad de reintegrarme el d�a "
							else:
								?? " , debiendose reintegrar el d�a "

							if i == 1:
								?? dtoc(ddreg) + " a mi primera"
								? "obligaci�n."
							else:
								? dtoc(ddreg) + " a su primera obligaci�n."

							?
							if i == 1:
								? " "
							else:
								? "        Sirva la presente de instrumento de notificaci�n fehaciente."

							?
							?
							?
							?
							?
							if i == 1:
								? "      ............................"
								nom_comp = alltrim(upper(ps -> apellido)) + ", " + alltrim(ps -> nombres)
								? padc(nom_comp,40," ")
								? "             Dependiente"
							else:
								? "      ............................"
								? "                                  "
								? "            p/EL FIDEO FELIZ"
							?
							?
							if afecta:
								match
									case nvo_saldo < 0
										reng1 = " ";
											+ padl(alltrim(str(vie_dlic)),2,"0");
											+ " dias de " ;
											+ padl(alltrim(str(vie_dlic)),2,"0");
											+ " / Licencia ";
											+ alltrim(str(year(vie_licc)));
											+ "   " ;
											+ padl(alltrim(str(resto)),2,"0");
											+ " dias de " ;
											+ padl(alltrim(str(dias_lic)),2,"0");
											+ " / Licencia ";
											+ alltrim(str(year(vlic_curso)))
									
									case nvo_saldo > 0
											# ARREGLAR ACA PARA QUE APAREZCA EL
											# EL TOTAL DE LOS DIAS YA TOMADOS
											# reng1 = padl(alltrim(str(        em -> cantidad        ),2,"0"));
											#
										reng1 = " ";
											+ padl(alltrim(str(diasytom + em -> cantidad)),2,"0");
											+ " dias de " ;
											+ padl(alltrim(str(dias_lic)),2,"0");
											+ " / Licencia ";
											+ alltrim(str(year(vlic_curso)))
										
									case nvo_saldo = 0
										reng1 = " ";
											+ padl(alltrim(str(vie_dlic)),2,"0");
											+ " dias de " ;
											+ padl(alltrim(str(vie_dlic)),2,"0");
											+ " / Licencia ";
											+ alltrim(str(year(vie_licc)))

							else:
								reng1 = " "

							if i == 1:
								? ""
							else:
								? reng1

							if i == 1:
								?
								?
								?
							else:
								eject


						#
						set console on
						set printer off
						set printer to
				else:
					son = alert ("  El empleado no se encontr� ; � Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1

				close em
			#
			# 1
			#


		case '2'
			while True: # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,16,78," 5.2. CONSULTA INDIVIDUAL SOBRE LICENCIAS ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@  6,2 say "���������������������������������������������������������������������������ĺ"
				@ 14,2 say "���������������������������������������������������������������������������ĺ"
				#
				@ 4,4 say "C�digo de Empleado :" get vcemp picture "999"
				set cursor on
				read
				set cursor off
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return

				ps -> (dbgotop())
				ps -> (dbseek(vcemp))
				if ps -> (found()):
					@  4,30 say alltrim(ps ->apellido) + ", " + alltrim(ps -> nombres)
					@  8,4  say "Licencia en Curso correspondiente a : " + str(ps -> lic_curso,4)
					@ 10,4  say "      Saldo de la Licencia en Curso : " + str(ps -> saldo_lic,2) + " d�as "
					@ 12,4  say "Fecha de regreso de �ltima licencia : " + dtoc(ps -> fe_regreso)
					@ 15,4  say "PRESIONE [ENTER] PARA CONSULTAR POR OTRO DEPENDIENTE [ESC] PARA SALIR"
					son = inkey(0)
					if son == K_ESC:
						exit # 1
					else:
						loop # 1
				else:
					son = alert ("  El empleado no se encontr� ; � Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1
					endif
				endif
			#
			enddo # 1
			#
			
		case elec3 = 3
			while True # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,16,78," 5.2. LISTADO DE SALDOS DE LICENCIAS ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@  6,2 say "���������������������������������������������������������������������������ĺ"
				@ 14,2 say "���������������������������������������������������������������������������ĺ"
				#
				@ 4,4 say "Por pantalla [P] o por impresora [i]:" get pimp ;
					valid pimp = "P" or pimp = "I";
					picture "@!"
				set cursor on
				read
				set cursor off
				if lastkey() = K_ESC
					restscreen(0,0,23,79,sc)
					close all
					return
				endif
				if pimp = "P"
					set console off
					set printer off
					set alternate to co_sdlic.txt
					set alternate on
					@ 10,16 clear to 14,70
					@ 10,16 to 14,70 double
					color_vie = setcolor()
					setcolor("n*/w")
					@ 12,17 say " PROCESANDO...    Espere por favor!!! "
					setcolor(color_vie)
				else:
					set console off
					set printer on
					set printer to (prtimp3)
				#
				encab_lsl(elec3)
				#
				#
				ps -> (dbsetorder(2))
				ps -> (dbgotop())
				while !(ps -> (eof())): # 2
				#
					vlic_curso = ctod(
							str(day(ps -> f_ing))+ "/" +
							str(month(ps -> f_ing))+ "/" +
							# ACA ANTES LE SUMABA 1
							# str(ps -> lic_curso + 1)
							str(ps -> lic_curso);
							)
					# 
					# CALCULO DE LOS DIAS DE LICENCIA
					#
					dias_lic = dias_d_lic(ps -> f_ing , vlic_curso)
					#
					nom_comp = padr((alltrim(ps -> apellido) + ", " + alltrim(ps -> nombres)),37, " ")
					? nom_comp
					+ space(2) + str(ps -> lic_curso,4)					# LIC EN CURSO
					+ space(8) + str(dias_lic,2) 						# TOTAL LIC
					+ space(9) + str((dias_lic - ps -> saldo_lic),2)	# LIC TOMADA
					+ space(9) + str(ps -> saldo_lic,2) 				# SALDO LIC
					?
					#
					ps -> (dbskip())
				#
				# 2
				ps -> (dbsetorder(1))
				? "-------------------------------------------------------------------------------"
				if pimp == "P":
					@  3,0 say padc((" LICENCIAS DEL PERSONAL - LISTADO DE SALDOS "),80,"�")
					@ 22,0 say "��������������������������������������������������������������������������������"
					set alternate off
					close alternate
					set console on
					browtext (4,0,21,79,(dirbase + "co_sdlic.txt"),False)
					loop # 1
			#
			# 1
			#

		case '4':
			while True: # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,16,78," 5.4. RESUMEN DE LICENCIAS DEL DEPENDIENTE ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@  6,2 say "���������������������������������������������������������������������������ĺ"
				@ 14,2 say "���������������������������������������������������������������������������ĺ"
				#
				@ 4,4 say "C�digo de Empleado :" get vcemp picture "999"
				set cursor on
				read
				set cursor off
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return
				ps -> (dbgotop())
				ps -> (dbseek(vcemp))
				if ps -> (found()):
					@  4,30 say alltrim(ps ->apellido) + ", " + alltrim(ps -> nombres)
					@  8,4  say "C�digo de Licencia : " get evento ;
						picture "99" 
					@ 10,38 say "FECHA INICIAL DE CONSULTA :" get finr
					@ 11,38 say "  FECHA FINAL DE CONSULTA :" get ffir valid ffir >= finr
					set cursor on
					read
					set cursor off
					if lastkey() == K_ESC:
						restscreen(0,0,23,79,sc)
						close all
						return

					select ev
					ev -> (dbgotop())
					locate for ev -> cd_evento = evento
					if ev -> (found()):
						@ 6,32 say ev -> desc
					else:
						tone(100,3)
						alert ("C�digo de Licencia inexistente...")
						loop # 2
				else:
					son = alert ("  El empleado no se encontr� ; � Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1

				if empty(finr):
					finr = ctod("01/01/03") # FECHA DE LA PRIMER LICENCIA REGISTRADA EN EL SIG

				if empty(ffir):
					ffir = date()

				@ 15,4 say "Por pantalla [P] o por impresora [I]:" get pimp valid pimp = "P" or pimp = "I" picture "@!"
				set cursor on
				read
				set cursor off
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return

				if pimp == "P":
					set console off
					set printer off
					set alternate to co_rslic.txt
					set alternate on
					@ 10,16 clear to 14,70
					@ 10,16 to 14,70 double
					color_vie = setcolor()
					setcolor("n*/w")
					@ 12,17 say " PROCESANDO...    Espere por favor!!! "
					setcolor(color_vie)
				else:
					set console off
					set printer on
					set printer to (prtimp3)
				#
				encab_lsl(elec3)
				#

				#
				# APERUTRA DEL ARCHIVO (LEGAJO) DEL EMPLEADO
				#
				archivo = "LEG_" + padl(alltrim(str(vcemp)),3,"0")
				archivoc = dirb6 + archivo + ".dbf"
				#
				use (archivoc);
					index (dirb6 + archivo + ".ntx");
					alias em new
				select em
				if evento != 0:
					set filter to (em -> desde >= finr and em -> hasta <= ffir) and em -> motivo = evento
				else:
					set filter to em -> desde >= finr and em -> hasta <= ffir
				endif
				em -> (dbgotop())
				#
				while !(em ->(eof())): # 2
				#





				#
				# 2
				close em
				#

			#
			# 1
			#

	restscreen(0,0,23,79,sc)
	close all
	return
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
def dias_d_lic(f_ing,f_ref):
#
	#
	private dt
	#
	dt = (f_ref - f_ing) + 1
	match dt:
		case 1825: 		# de 0 a 5 a�os - 1 dia
			return 14
			
		case 3650:		# de 5 a 10 a�os - 1 dia
			return 21
			
		case 7300:		# de 10 a 20 a�os - 1 dia
			return 28
			
		case > 7300:	# 20 a�os o mas
			return 35
			
	endcase
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
def encab_lsl(elec3):
	#
	cant_lin = pag = 0

	if pimp = "I":
		printcodes(chr(27)+chr(33)+chr(0))

	? "-------------------------------------------------------------------------------"
	if pimp = "I":
		printcodes(chr(27)+chr(33)+chr(96))

	pag ++
	? "EL FIDEO FELIZ"
	if pimp = "I":
		printcodes(chr(27)+chr(33)+chr(64))

	?? " de Jose F. Pes"
	?? space(28) + dtoc(date())
	? "Perito Moreno 276, Rawson.(CH) - Tel/Fax (0280) 448-2993"
	?? space(15) + "Pag. " + str(pag,3)
	?
	if pimp = "I":
		printcodes(chr(27)+chr(33)+chr(16))
	
	match elec3
		case '3':
			? "LICENCIAS DEL PERSONAL - LISTADO DE SALDOS"
			if pimp = "I":
				printcodes(chr(27)+chr(33)+chr(0))

			#if !(empty(vzona)):
			#	? "(Zona " + ps -> cod_zona + ")"
			#
			? "-------------------------------------------------------------------------------"
			? " APELLIDO Y NOMBRE(S)                 LICENCIA    TOTAL     LICENCIA    SALDO  "
			? "                                      EN CURSO   LICENCIA    TOMADA    LICENCIA"
			? "-------------------------------------------------------------------------------"
			#  123456789 123456789 123456789 1234567  1234        12         12         12
			#  123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345678
			
		case '4'
			? "RESUMEN DE LICENCIAS DEL DEPENDIENTE"
			if pimp = "I":
				printcodes(chr(27)+chr(33)+chr(0))

			? upper(alltrim(ps -> apellido) + ", " + ps -> nombres)
			? "-------------------------------------------------------------------------------"
			? " APELLIDO Y NOMBRE(S)                 LICENCIA    TOTAL     LICENCIA    SALDO  "
			? "                                      EN CURSO   LICENCIA    TOMADA    LICENCIA"
			? "-------------------------------------------------------------------------------"
			#  123456789 123456789 123456789 1234567  1234        12         12         12
			#  123456789 123456789 123456789 123456789 123456789 123456789 123456789 12345678

	#
	#
	return
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#
#
#
#
#
#