#include "inkey.ch"
#
# NOVEDADES
#
def rh_noved(elec3):
	#
	private evento,finie,ffine,nvo_saldo,archivo,archivoc,resto,j
	private dias_lic, vlic_curso
	#
	vcemp = 0
	j = 1
	i = 0
	sepa = False
	cdv6 = 0
	evento = 0
	finie = ctod("  /  /  ")
	ffine = ctod("  /  /  ")
	nvo_saldo = 0
	resto = 0
	dias_lic = 0
	vlic_curso = ctod("  /  /  ")
	imp_fa = "    "
	#
	use(dirb6+"personal") index (dirb6+"persona1"),(dirb6+"persona2"),(dirb6+"persona3") alias ps new
	use(dirb6+"categori") alias ct new
	use (dirb6+"est_civ") alias ec new
	use (dirb6+"tipo_doc") alias td new
	use (dirb6+"eventos") alias ev new
	#
	restore from impresos.mem additive
	#
	match elect3:
		case '1':
			while True: # 1
				restscreen(0,0,23,79,sc)
				spcaja (3,2,16,78," 5.3. INGRESO DE NOVEDADES EN EL LEGAJO ";
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
						@ 6,4  say "Descripci�n del Evento :" get evento picture "99" valid left(str(evento,2),1) = "2"
						set cursor on
						read
						set cursor off
						if lastkey() == K_ESC:
							restscreen(0,0,23,79,sc)
							close all
							return

						ev -> (dbgotop())
						locate for ev -> cd_evento == evento
						if ev -> (found()):
							@ 6,32 say ev -> desc
						else:
							tone(100,3)
							alert ("  Evento inexistente...  ")
							loop # 2

						exit # 2
					#
					# 2
					#
					@ 8,4 say "Evento producido desde el          hasta el "
					@ 8,30 get finie
					set cursor on
					read
					set cursor off
					ffine = finie
					@ 8,48 get ffine valid ffine >= finie
					set cursor on
					read
					set cursor off
					if lastkey() == K_ESC:
						restscreen(0,0,23,79,sc)
						close all
						return
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
					#
					son = alert ("�Imprime la planilla correspondiente?", {" SI "," NO "})
					if son == 1:
						#
						# RUTINA PARA IMPRIMIR
						# LA PLANILLA DEL EVENTO
						# QUE CORRESPONDA
						#
				else:
					son = alert ("  El empleado no se encontr� ; � Desea intentar con otro ? ",{" SI "," NO "})
					if son == 2:
						exit # 1
					else:
						restscreen(0,0,23,79,sc)
						loop # 1
			#
			# 1
			#

	restscreen(0,0,23,79,sc)
	close all
	return
	#
	#
	#
	#
	#
	#
	#
	#
	#