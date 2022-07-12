#
#
#
def rrhhAdmPersonal(elec3):
#
	public vcemp, vtipo, vparent
	private vven, vprov, vzon, vd, addv
	#
	vcemp = 0
	j = 1
	i = 0
	z = 0
	sepa = False
	cdv6 = 0
	opc = 0
	archf = ""
	archl = ""
	legajo = 0
	vtipo = 0
	vparent = 0
	#
	use(dirb6+"personal") index (dirb6+"persona1"),(dirb6+"persona2"),(dirb6+"persona3") alias ps new
	use(dirb6+"categori") alias ct new
	use(dirb6+"est_civ") alias ec new
	use(dirb6+"tipo_doc") alias td new
	use(dirb6+"parent") alias pt new
	#
	match elec3:

		case '1':
			while True: # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,20,78," 5.1.1. MODIFICACION DATOS DE EMPLEADOS ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				vcemp = imput("CODIGO DE EMPLEADO :" )
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return
				#
				ps -> (dbgotop())
				ps -> (dbseek(vcemp))
				if ps -> (found()):
					ps -> apellido = input("        APELLIDO :") valid !empty(ps -> apellido) 
					ps -> nombres = input("         NOMBRES :") valid !empty(ps -> nombres) 
					@  9,3  say " TIPO y N° de DOC. :" get ps -> tipo;
						valid !empty(ps -> tipo) 
					@  9,26 get ps -> docu;
						valid !empty(ps -> docu) 
					@ 10,3  say "        C.U.I.L. :" get ps -> cuil;
						valid !empty(ps -> cuil) 
					@ 11,3  say " FECHA NACIM.:" get ps -> f_nac
					@ 11,27 say " FECHA INGRESO :" get ps -> f_ing
					@ 11,53 say " FECHA EGRESO :" get ps -> f_egre
					@ 12,3  say " CATEGORIA :" get ps -> categ 
					@ 12,47 say " EST. CIVIL :" get ps -> est_civil
					@ 13,3  say "��������������������������������������������������������������������������"
					@ 14,7  say " DOMICILIO :" get ps -> domicilio
					@ 15,7  say " LOCALIDAD :" get ps -> localidad
					@ 15,47 say " CODIGO POSTAL :" get ps -> cp
					@ 16,3  say " TELEFONO :" get ps -> tel
					@ 17,3  say "��������������������������������������������������������������������������"
					@ 18,3  say " COMISION : "
					set cursor on
					read
					set cursor off
					if ps -> categ == 6:
						@ 18,15 get ps -> comision picture "99.99";
							valid ps -> comision > -1
						set cursor on
						read
						set cursor off
					#
					# RUTINA PARA MODIF. DATOS GRUPO FAMILIAR
					#
					opc = ing_flia(ps -> cod_emp)
					#
					#
					#
					son = alert (" � Desea modificar otro  ; empleado o salir ?      ",{" Otro ","Salir"})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1
				else:
					son = alert ("  El empleado no se encontr� ; � Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1
			#
			#
		case '2':
			while True: # 2
			#
				restscreen(0,0,23,79,sc)
				spcaja (3,2,8,78," 5.1.2. BAJA DE EMPLEADOS ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@ 4,4 say "CODIGO DE EMPLEADO :" get vcemp picture "999"
				set cursor on
				read
				set cursor off
				if lastkey() == K_ESC:
					restscreen(0,0,23,79,sc)
					close all
					return
				#
				select ps
				ps -> (dbgotop())
				ps -> (dbseek(vcemp))
				if found():
					cadena = "El Empleado que corresponde al c�digo ingresado es ; ;" ;
						+ ">" + padc((alltrim(ps -> apellido) + ", " + alltrim(ps -> nombres)),50,"�") + "<" ;
						+ " ; ; " ;
						+ " ¿ Desea darlo de baja o intentar con otro código ? "
					son = alert( cadena ,{" Baja "," Otro "})
					if son == 1:
						select ps
						ps -> (dbdelete())
						pack
						exit # 2
				else:
					son = alert("  El empleado no se encontró ; ¿ Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 2
					else:
						restscreen(0,0,23,79,sc)
						loop # 2
			# 2
			#
			#
			
		case '3':
			while True: # 2
			#
				select ps
				ps -> (dbgobottom())
				legajo = ps -> cod_emp + 1
				ps -> (dbappend())
				replace ps -> cod_emp with legajo
				#
				restscreen(0,0,23,79,sc)
				spcaja (3,2,20,78," 5.1.3. ALTA DE EMPLEADOS ";
					,(isc),(isc),(isc4),(menubox);
					,False)
				@  4,23  say "L E G A J O    N � :" + padl(alltrim(str(ps -> cod_emp)),3,"0")

				@  6,3  say "        APELLIDO :" get ps -> apellido;
					valid !empty(ps -> apellido) 
				@  7,3  say "         NOMBRES :" get ps -> nombres;
					valid !empty(ps -> nombres) 
				@  9,3  say " TIPO y N� de DOC. :" get ps -> tipo;
					valid !empty(ps -> tipo) 
				@  9,26 get ps -> docu;
					valid !empty(ps -> docu) 
				@ 10,3  say "        C.U.I.L. :" get ps -> cuil;
					valid !empty(ps -> cuil) 
				@ 11,3  say " FECHA NACIM.:" get ps -> f_nac
				@ 11,27 say " FECHA INGRESO :" get ps -> f_ing
				@ 11,53 say " FECHA EGRESO :" get ps -> f_egre
				@ 12,3  say " CATEGORIA :" get ps -> categ 
				@ 12,47 say " EST. CIVIL :" get ps -> est_civil
				@ 13,3  say "��������������������������������������������������������������������������"
				@ 14,7  say " DOMICILIO :" get ps -> domicilio
				@ 15,7  say " LOCALIDAD :" get ps -> localidad
				@ 15,47 say " CODIGO POSTAL :" get ps -> cp
				@ 16,3  say " TELEFONO :" get ps -> tel
				@ 17,3  say "��������������������������������������������������������������������������"
				@ 18,3  say " COMISION : "
				set cursor on
				read
				set cursor off
				#
				# INGRESO DE LICENCIA EN CURSO Y SALDO DE DIAS 
				#
				replace ps -> lic_curso with year(ps -> f_ing)
				replace ps -> saldo_lic with 14
				#
				#
				#
				if ps -> categ == 6:
					@ 18,15 get ps -> comision picture "99.99";
						valid ps -> comision > -1
					set cursor on
					read
					set cursor off
				#
				if lastkey() == K_ESC:
					select ps
					ps -> (dbdelete())
					pack
					exit # 2
				#
				# CREAR EL LEGAJO PERSONAL Y EL ARCHIVO DE FAMILIA
				#
				archl = dirb6 + "leg_" + padl(alltrim(str(legajo)),3,"0")
				copy file (dirb6+"cc_licen.dbf") to (archl + ".dbf")
				copy file (dirb6+"cclicen1.ntx") to (archl + ".ntx")
				#
				archf = dirb6 + "flia_" + padl(alltrim(str(legajo)),3,"0")
				copy file (dirb6+"familias.dbf") to (archf + ".dbf")
				copy file (dirb6+"familias.ntx") to (archf + ".ntx")
				#
				#
				# RUTINA PARA MODIF. DATOS GRUPO FAMILIAR
				#
				opc = ing_flia(ps -> cod_emp)
				#
				#
				#
				son = alert(" Confirma los datos ingresados ; del empleado ?                ",{"  SI  ","  NO  "})
				if son == 1:
					son = alert(" �Desea ingresar otro empleado ; o finalizar y salir ?         ",{" Otro ","Salir"})
					if son == 2:
						exit # 2
					else:
						restscreen(0,0,23,79,sc)
						loop # 1
				else:
					select ps
					ps -> (dbdelete())
					pack
					exit # 2
			#

		case '4':
			restscreen(0,0,23,79,sc)
			spcaja (3,20,14,60," 5.1.4. IMPRESION DE LISTADO DE EMPLEADOS ";
				,(isc),(isc),(isc4),(menubox);
				,False)
			while True: # 1
				@ 4,25 say "Escoja el orden del listado :"
				@       6,28 prompt " 1. x C�digo de Empleado"
				@ row()+1,28 prompt " 2. x Fecha de Ingreso  "
				@ row()+1,28 prompt " 3. En orden Alfab�tico "
				menu to son
				select ps
				set index to
				match son:
					case '0':
						restscreen(0,0,23,79,sc)
						close all
						return
					
					case '1':
						select ps
						set order to 1
						mensaje = "por c�digo de empleado"
						
					case '2':
						set order to 3
						mensaje = "por fecha de ingreso"
						
					case '3':
						set order to 2
						mensaje = "alfab�tico - nombre"

				exit # 1
			# 1
			set console off
			set printer on
			set printer to (prtimp3)
			enc_admp(mensaje)
			if son == 6:
				for s in range(1,7):
					printcodes(chr(27)+chr(33)+chr(96))
					? addv[s+1]
					printcodes(chr(27)+chr(33)+chr(0))
					locate for ps -> dvis = s
					printcodes(chr(27)+chr(33)+chr(1))
					while !(eof()) and ps -> dvis = s: # 1
						sepa = True
						i ++
						? ps -> cod_suc + ps -> provincia + ps -> zona + str(ps -> cod_cli,4),;
						ps -> nom_fanta,;
						ps -> domicilio,;
						left(ps -> localidad,10),;
						ps -> cuit
						ps -> (dbskip())
						if i == 56:
							printcodes(chr(27)+chr(33)+chr(4))
							? "Sigue..."
							printcodes(chr(27)+chr(33)+chr(0))
							eject
							enc_admp(mensaje)
							i = 0
						endif
					enddo # 1
					if sepa == True:
						?

					ps -> (dbgotop())
					printcodes(chr(27)+chr(33)+chr(1))
					while !(eof()) and ps -> dvis == 0: # 1
						i ++
						? ps -> cod_suc + ps -> provincia + ps -> zona + str(ps -> cod_cli,4),;
						ps -> nom_fanta,;
						ps -> domicilio,;
						left(ps -> localidad,10),;
						ps -> cuit
						ps -> (dbskip())
						if i == 56:
							printcodes(chr(27)+chr(33)+chr(4))
							? "Sigue..."
							printcodes(chr(27)+chr(33)+chr(0))
							eject
							enc_admp(mensaje)
							i = 0

					# 1
					if s < 6:
						printcodes(chr(27)+chr(33)+chr(0))
						eject
						enc_admp(mensaje)
						i = 0
				? "--------------------------------------------------------------------------------"
			else:
				select ps
				ps -> (dbgotop())
				printcodes(chr(27)+chr(33)+chr(4))
				while !(eof()): # 1
					i ++
					? ps -> cod_suc + ps -> provincia + ps -> zona + str(ps -> cod_cli,4),;
					ps -> nom_fanta,;
					ps -> razon_soc,;
					ps -> cuit,;
					ps -> sit_imp,;
					ps -> domicilio,;
					ps -> localidad,;
					ps -> cp
					ps -> (dbskip())
					if i == 56:
						? "Sigue..."
						eject
						enc_admp(mensaje)
						i = 0
				# 1
				? "--------------------------------------------------------------------------------"
			printcodes(chr(27)+chr(33)+chr(0))
			? "Total de clientes - " + tsu + " : " + str(ps -> (lastrec()))
			eject
			set printer off
			set console on

	restscreen(0,0,23,79,sc)
	close all
	return
	#
	#
	#
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	#
	procedure enc_admp(mensaje)
	#
	printcodes(chr(27)+chr(33)+chr(0))
	? "--------------------------------------------------------------------------------"
	printcodes(chr(27)+chr(33)+chr(96))
	? "EL FIDEO FELIZ"
	printcodes(chr(27)+chr(33)+chr(64))
	?? " de Jose F. Pes"
	?? space(29) + dtoc(date())
	? "Perito Moreno 276, Rawson.(CH) - Tel/Fax (0280) 448-2993"
	?? space(18) + "Pag. " + str(j,3)
	?
	printcodes(chr(27)+chr(33)+chr(16))
	? "Listado de Clientes "
	?? mensaje
	printcodes(chr(27)+chr(33)+chr(0))
	? tsu
	if son == 6:
		printcodes(chr(27)+chr(33)+chr(1))
		? "------------------------------------------------------------------------------------------------"
		? "C�digo     Nombre de Fantas�a                   Domicilio          Localidad           CUIT"
		? "------------------------------------------------------------------------------------------------"
	else:
		printcodes(chr(27)+chr(33)+chr(4))
		? "----------------------------------------------------------------------------------------------------------------------------------------"
		? "  C�digo       Nombre de Fantas�a            Raz�n Social            C.U.ITrue     IVA        Domicilio            Localidad         C.P."
		? "----------------------------------------------------------------------------------------------------------------------------------------"
	j ++ 
	return
	#
	#
	#
	#
	#
	#
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	# 
	def ing_flia(legajo):
		"""
		FUNCION PARA INGRESO DE FAMILIARES
		"""
		public aop,aop2

		archivoc = " "
		aop = {}
		aop2 = {}
		#
		#
		archivoc = dirb6 + "flia_" + padl(alltrim(str(legajo)),3,"0") + ".dbf"
		use (archivoc) index (archivoc) alias fl new
		#
		select fl
		fl -> (dbgotop())
		#
		if fl -> (lastrec()) > 0:
			while !(fl -> (eof())): # 2
				reng_fl =   "  " + fl -> apellido;
					+ " � " + fl -> nombre;
					+ " � " + str(fl -> parent,1);
					+ " � " + dtoc(fl -> f_nac);
					+ " � " + str(fl -> tipo,1);
					+ " � " + fl -> docu;
					+ "  " 
				aadd(aop,reng_fl)
				aadd(aop2," ")
				fl -> (dbskip())
			# 2
		else:
			reng_fl =   "  " + " N  U  E  V  O ";
				+ " � " + " ENTER  p/Modificar ";
				+ " � " + " ";
				+ " � " + space(8);
				+ " � " + " ";
				+ " � " + space(8);
				+ "  " 
			aadd(aop,reng_fl)
			aadd(aop2,"A")
		#
		while True: # 1
			#
			vapellido = space(15)
			vnombre = space(20)
			vparent = 0
			vf_nac = ctod("  /  /  ")
			vtipo = 0
			vdocu = space(8)
			#
			spcaja (3,2,21,78," INGRESO DE DATOS GRUPO FAMILIAR DE EMPLEADOS ";
				,(isc),(isc),(isc4),(menubox);
				,False)
			while True: # 2
				@ 4,3 clear to 11,74
				@ 4,3,11,74 box B_SINGLE
				for i in range(1,7):
					@ 4+i,4 say space(17) + " � ";
						+ space(20) + " � ";
						+ " " + " � ";
						+ space(8) + " � ";
						+ " " + " � "

				@ 13,4  say "Apellido :" 
				@ 13,32 say "Nombres :" 
				@ 15,4  say "Parentesco :"
				@ 17,4  say "Fecha de Nacimiento:"
				@ 19,4  say "Tipo de Doc.:"
				@ 19,20 say "N� :"
				#
				caca = achoice(5,4,10,72,aop,,"achofunf")
				if caca == 0:
					if lastkey() != K_ESC:
						loop # 2
					else
						son = alert("�Confirma los datos ingresados;o desea cancelar la edici�n?",{" Confirma "," Cancelar "})
						if son = 1
							# CONFIRMA EDICION DE DATOS
							select fl
							fl -> (dbgotop())
							#
							z = 0
							do while z < len(aop) # 2
								z ++
								do case
									case aop2[z] = "M"
										fl -> (dbgoto(z))
										replace fl -> apellido with substr(aop[z],3,15)
										replace fl -> nombre   with substr(aop[z],21,20)
										replace fl -> parent   with val(substr(aop[z],44,1))
										replace fl -> f_nac    with ctod(substr(aop[z],48,8))
										replace fl -> tipo     with val(substr(aop[z],59,1))
										replace fl -> docu     with substr(aop[z],63,8)
										
									case aop2[z] = "A"
										select fl
										fl -> (dbappend())
										replace fl -> apellido with substr(aop[z],3,15)
										replace fl -> nombre   with substr(aop[z],21,20)
										replace fl -> parent   with val(substr(aop[z],44,1))
										replace fl -> f_nac    with ctod(substr(aop[z],48,8))
										replace fl -> tipo     with val(substr(aop[z],59,1))
										replace fl -> docu     with substr(aop[z],63,8)
										
									case aop2[z] = "B"
										select fl
										delete record (z)
										pack
								endcase
							enddo # 2
							#
						endif
						fl ->(dbclosearea())
						return 1 # VUELVE 
					endif
				endif 
			enddo # 2
		enddo # 1
	#
	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
	#
	def achofunf(modo,op,pos):
		private nvoreng
		#
		match modo:
			case '3':
				if lastkey() == K_ENTER:
					vapellido = substr(aop[op],3,15)
					vnombre = substr(aop[op],21,20)
					vparent = val(substr(aop[op],44,1))
					vf_nac = ctod(substr(aop[op],48,8))
					vtipo = val(substr(aop[op],59,1))
					vdocu = substr(aop[op],63,8)
					@ 13,14 get vapellido picture "@!K"
					@ 13,42 get vnombre picture "@!K"
					@ 15,17 get vparent picture "9"
					@ 17,25 get vf_nac
					@ 19,18 get vtipo picture "9"
					@ 19,25 get vdocu picture "99999999" valid val(vdocu) > -1
					set cursor on
					read
					set cursor off
				if lastkey() == K_ESC:
					return 2 # continuar achoice

				nvoreng =  "  " + vapellido;
					+ " � " + vnombre;
					+ " � " + str(vparent,1);
					+ " � " + dtoc(vf_nac);
					+ " � " + str(vtipo,1);
					+ " � " + vdocu;
					+ "  " 
				aop[op] = nvoreng
				if aop2[op] != "A":
					aop2[op] = "M"

			case '3':
				if lastkey() == K_INS:
					vapellido = ps -> apellido # space(15)
					vnombre = space(20)
					vparent = 0
					vf_nac = ctod("  /  /  ")
					vtipo = 0
					vdocu = space(8)
					@ 13,14 get vapellido picture "@!K"
					@ 13,42 get vnombre picture "@!K"
					@ 15,17 get vparent picture "9"
					@ 17,25 get vf_nac
					@ 19,18 get vtipo picture "9"
					@ 19,25 get vdocu picture "99999999" valid val(vdocu) > -1
					set cursor on
					read
					set cursor off
				if lastkey() == K_ESC:
					return 2 # continuar achoice

				nvoreng =  "  " + vapellido;
					+ " � " + vnombre;
					+ " � " + str(vparent,1);
					+ " � " + dtoc(vf_nac);
					+ " � " + str(vtipo,1);
					+ " � " + vdocu;
					+ "  " 
				aadd(aop,nvoreng)
				aadd(aop2,"A")
				return 0 # abortar achoice
				
			case '3'
				if lastkey() == K_DEL:
					if aop2[op] == "A":
						adel(aop[op])
						adel(aop2[op])
						asize(aop,len(aop)-1)
						asize(aop2,len(aop2)-1)
					else:
						# aop2[op] = " " or aop2[op] = "M"
						aop2[op] = "B"
						vapellido = " B O R R A D O "
						vnombre = space(20)
						vparent = 0
						vf_nac = ctod("  /  /  ")
						vtipo = 0
						vdocu = space(8)
						aop[op] = "  " + vapellido;
							+ " � " + vnombre;
							+ " � " + str(vparent,1);
							+ " � " + dtoc(vf_nac);
							+ " � " + str(vtipo,1);
							+ " � " + vdocu;
							+ "  "

				return 0 # abortar achoice

			case lastkey() == K_ESC:
				return 0 # abortar achoice

		return 2 # continuar achoice
#
#
#
#
#
#
#
#