from flask import Flask, flash
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
import calcula_licencia as cl
from pprint import pprint
import datetime as dt
import tempfile
import win32api
import win32print

app = Flask(__name__)
app.secret_key = 'Clave'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'rrhh'
mysql.init_app(app)


MY_PATH = os.path.dirname(os.path.abspath(__file__))
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA
app.secret_key = 'Clave'


@app.route('/uploads/<nombreImg>')
def uploads(nombreImg):
    return send_from_directory(app.config['CARPETA'], nombreImg)


@app.route('/')
def index():
    sql = 'SELECT * FROM rrhh.personal ORDER BY apellidos, nombres;'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    return render_template('rrhh/index.html', empleados=empleados)


# PARA MOSTRAR LOS DATOS DE UN EMPLEADO SIN EDITARLOS
@app.route('/show/<int:id_empleado>')
def show(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM rrhh.personal WHERE id_empleado=%s', (id_empleado))
    empleado = cursor.fetchone()

    cursor.execute('SELECT * FROM rrhh.tipo_doc WHERE id_documento=%s;', empleado[5])
    id_doc_empleado, tipo_doc_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.tipo_doc;'
    cursor.execute(sql)
    tipo_docs = cursor.fetchall()

    cursor.execute('SELECT * FROM rrhh.est_civil WHERE id_est_civil=%s;', empleado[12])
    id_est_civ_empleado, tipo_est_civ_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.est_civil;'
    cursor.execute(sql)
    est_civiles = cursor.fetchall()

    cursor.execute('SELECT * FROM rrhh.categorias WHERE id_categoria=%s;', empleado[11])
    id_categ_empleado, tipo_categ_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.categorias;'
    cursor.execute(sql)
    categorias = cursor.fetchall()

    sql = 'SELECT id_localidad, nombre FROM rrhh.localidades WHERE id_localidad=%s;'
    cursor.execute(sql, empleado[14])
    id_local_empleado, nombre_local_empleado = cursor.fetchone()

    sql = 'SELECT id_provincia, nombre FROM rrhh.provincias WHERE id_provincia=%s;'
    cursor.execute(sql, empleado[15])
    id_prov_empleado, nombre_prov_empleado = cursor.fetchone()
    id_loc_prov_empleado = str(id_local_empleado) + '-' + str(id_prov_empleado)
    lyp_completo_empleado = nombre_local_empleado + ' - ' + nombre_prov_empleado

    sql = '''SELECT 
                CONCAT(loc.id_localidad,'-',prov.id_provincia) AS loc_prov,
                CONCAT(loc.nombre, ' - ', prov.nombre) AS lyp_completo  
                FROM rrhh.localidades AS loc
                JOIN rrhh.provincias AS prov
                WHERE loc.id_provincia = prov.id_provincia
                ORDER BY lyp_completo;'''
    cursor.execute(sql)
    locs_y_provs = cursor.fetchall()

    return render_template('rrhh/show.html',
        empleado=empleado,
        id_doc_empleado=id_doc_empleado,
        tipo_doc_empleado=tipo_doc_empleado,
        documentos=tipo_docs,
        id_est_civ_empleado=id_est_civ_empleado,
        tipo_est_civ_empleado=tipo_est_civ_empleado,
        est_civiles=est_civiles,
        id_categ_empleado=id_categ_empleado,
        tipo_categ_empleado=tipo_categ_empleado,
        categorias=categorias,
        id_loc_prov_empleado=id_loc_prov_empleado,
        lyp_completo_empleado=lyp_completo_empleado,
        locs_y_provs=locs_y_provs,
        )


# PARA INGRESAR LOS PARAMETROS DE FILTRADO DEL PADRON DE EMPLEADOS
@app.route('/filter')
def filter():
    return render_template('rrhh/filter.html')


# PARA FILTRAR EL PADRON DE EMPLEADOS UNA VEZ INGRESADOS PARAMETROS DE FILTRO
@app.route('/filtered', methods=['POST'])
def filtered():
    apellidos = request.form['txtApellidos'].upper()
    nombres = request.form['txtNombres'].upper()

    if nombres != '' and apellidos != '':
        sql = f'''SELECT * FROM rrhh.personal WHERE 
                    LOCATE("{apellidos}", apellidos) > 0 
                    AND 
                    LOCATE("{nombres}", nombres) > 0 
                    ORDER BY apellidos, nombres;'''
    elif apellidos != '':
        sql = f'''SELECT * FROM rrhh.personal WHERE 
                    LOCATE("{apellidos}", apellidos) > 0 
                    ORDER BY apellidos, nombres;'''
    elif nombres != '':
        sql = f'''SELECT * FROM rrhh.personal 
                    WHERE LOCATE("{nombres}", nombres) > 0 
                    ORDER BY apellidos, nombres;'''
    else:
        sql = 'SELECT * FROM rrhh.personal ORDER BY apellidos, nombres;'

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute(sql)
    empleados = cursor.fetchall()

    if empleados == ():
        flash(apellidos + ', ' + nombres + ' no existe en el padrón...!')
        return redirect(url_for('filter'))

    return render_template('rrhh/index.html', empleados=empleados)


# PARA CREAR UN NUEVO EMPLEADO
@app.route('/create')
def create():

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = 'SELECT * FROM rrhh.tipo_doc;'
    cursor.execute(sql)
    tipo_docs = cursor.fetchall()

    sql = 'SELECT * FROM rrhh.est_civil;'
    cursor.execute(sql)
    est_civiles = cursor.fetchall()

    sql = 'SELECT * FROM rrhh.categorias;'
    cursor.execute(sql)
    categorias = cursor.fetchall()

    sql = '''SELECT 
                CONCAT(loc.id_localidad,'-',prov.id_provincia) AS loc_prov,
                CONCAT(loc.nombre, ' - ', prov.nombre) AS lyp_completo  
                FROM rrhh.localidades AS loc
                JOIN rrhh.provincias AS prov
                WHERE loc.id_provincia = prov.id_provincia
                ORDER BY lyp_completo;'''
    cursor.execute(sql)
    locs_y_provs = cursor.fetchall()
    conn.close()

    return render_template('rrhh/create.html',
        documentos=tipo_docs,
        est_civiles=est_civiles,
        categorias=categorias,
        locs_y_provs=locs_y_provs
        )


# PARA GUARDAR UN NUEVO EMPLEADO
@app.route('/store', methods=['POST'])
def storage():
    img = request.files['txtImagen']
    apellidos = request.form['txtApellidos']
    nombres = request.form['txtNombres']
    id_tipo_doc = request.form['TipoDocSelect']
    nro_doc = request.form['txtDoc']
    cuil = request.form['txtCuil']
    fecha_nac = request.form['dateNacim']
    id_est_civil = request.form['EstCivilSelect']
    fch_ingreso = request.form['dateIngreso']
    id_categoria = request.form['CategSelect']
    domicilio = request.form['txtDomicilio']
    loc_y_prov = request.form['LocalidadSelect']
    id_localidad, id_provincia = loc_y_prov.split('-')
    tel = request.form['txtTel']
    mail = request.form['txtEmail']

    if img.filename == '' or apellidos == '' or nombres == '' or id_tipo_doc == '' or nro_doc == '' or cuil == '' or fecha_nac == '' or id_est_civil == '' or fch_ingreso == '' or id_categoria == '' or domicilio == '' or id_localidad == '' or id_provincia == '':
        flash('Faltan datos obligatorios!')
        return redirect(url_for('create'))

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''INSERT INTO rrhh.personal
            (apellidos, nombres, id_documento, documento,
            cuil, fecha_nacimiento, fecha_ingreso, id_categoria,
            id_est_civil, domicilio, id_localidad, id_provincia,
            tel, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''.format(apellidos, nombres, id_tipo_doc, nro_doc, cuil, fecha_nac, fch_ingreso, id_categoria, id_est_civil, domicilio, id_localidad, id_provincia, tel, mail)
    datos = (apellidos, nombres,
            id_tipo_doc, nro_doc, cuil,
            fecha_nac, fch_ingreso, id_categoria,
            id_est_civil, domicilio, id_localidad, id_provincia,
            tel, mail)
    cursor.execute(sql, datos)
    conn.commit()

    sql = 'SELECT id_empleado FROM rrhh.personal WHERE apellidos=%s AND nombres=%s;'.format(apellidos, nombres)
    cursor.execute(sql,(apellidos, nombres))
    nvo_empleado = cursor.fetchone()
    id_empleado = nvo_empleado[0]
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if img.filename != '':
        nuevo_nombre_img = str(id_empleado).zfill(3) + '_' + tiempo + '.' + img.filename.split(".")[-1]
        img.save(MY_PATH + '/uploads/' + nuevo_nombre_img)
        # img.save(os.path.join(app.config['CARPETA'], nuevo_nombre_img))

    # CALCULO LA LICENCIA EN CURSO Y LOS DIAS QUE LE CORRESPONDEN
    licen_curso, saldo_licen, fecha_regreso, _ = cl.calc_lic_en_curso(id_empleado, 'alta')
    #

    sql = '''UPDATE rrhh.personal 
            SET foto=%s, saldo_licencia=%s, licencia_curso=%s, fecha_regreso=%s WHERE id_empleado=%s;
            '''.format(nuevo_nombre_img, saldo_licen, licen_curso, fecha_regreso, id_empleado,)
    datos = (nuevo_nombre_img, saldo_licen, licen_curso, fecha_regreso, id_empleado)
    cursor.execute(sql, datos)

    conn.commit()
    conn.close()
    return redirect('/')


# PARA MODIFICAR LOS DATOS DE UN EMPLEADO
@app.route('/update', methods=['POST'])
def update():
    id_empleado = request.form['txtIdEmpleado']
    img = request.files['txtImagen']
    apellidos = request.form['txtApellidos'].upper()
    nombres = request.form['txtNombres'].upper()
    id_tipo_doc = request.form['TipoDocSelect']
    nro_doc = request.form['txtDoc']
    cuil = request.form['txtCuil']
    fecha_nac = request.form['dateNacim']
    id_est_civil = request.form['EstCivilSelect']
    fch_ingreso = request.form['dateIngreso']
    id_categoria = request.form['CategSelect']
    domicilio = request.form['txtDomicilio']
    loc_y_prov = request.form['LocalidadSelect']
    id_localidad, id_provincia = loc_y_prov.split('-')
    tel = request.form['txtTel']
    mail = request.form['txtEmail']

    if img.filename == '' or apellidos == '' or nombres == '' or id_tipo_doc == '' or nro_doc == '' or cuil == '' or fecha_nac == '' or id_est_civil == '' or fch_ingreso == '' or id_categoria == '' or domicilio == '' or id_localidad == '' or id_provincia == '':
        flash('Faltan datos obligatorios!')
        return redirect(url_for('update'))

    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if img.filename != '':
       nuevo_nombre_img = str(id_empleado).zfill(3) + '_' + tiempo  + '.' + img.filename.split(".")[-1]
       img.save(MY_PATH + '/uploads/' + nuevo_nombre_img)

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT foto FROM rrhh.personal WHERE id_empleado=%s;',id_empleado)
    registro = cursor.fetchone()
    os.remove(MY_PATH + '/uploads/' + registro[0])

    sql = '''UPDATE rrhh.personal
            SET foto=%s, apellidos=%s, nombres=%s, id_documento=%s, documento=%s,
            cuil=%s, fecha_nacimiento=%s, fecha_ingreso=%s, id_categoria=%s,
            id_est_civil=%s, domicilio=%s, id_localidad=%s, id_provincia=%s,
            tel=%s, email=%s
            WHERE id_empleado=%s;
            '''.format(nuevo_nombre_img, apellidos, nombres, id_tipo_doc, nro_doc,
                        cuil, fecha_nac, fch_ingreso, id_categoria,
                        id_est_civil, domicilio, id_localidad, id_provincia,
                        tel, mail, id_empleado)
    datos = (nuevo_nombre_img, apellidos, nombres, id_tipo_doc, nro_doc,
            cuil, fecha_nac, fch_ingreso, id_categoria,
            id_est_civil, domicilio, id_localidad, id_provincia,
            tel, mail, id_empleado)
    cursor.execute(sql, datos)

    conn.commit()
    conn.close()

    return redirect('/')


# PARA EDITAR LOS DATOS DE UN EMPLEADO
@app.route('/edit/<int:id_empleado>')
def edit(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM rrhh.personal WHERE id_empleado=%s', (id_empleado))
    empleado = cursor.fetchone()

    cursor.execute('SELECT * FROM rrhh.tipo_doc WHERE id_documento=%s;', empleado[5])
    id_doc_empleado, tipo_doc_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.tipo_doc;'
    cursor.execute(sql)
    tipo_docs = cursor.fetchall()

    cursor.execute('SELECT * FROM rrhh.est_civil WHERE id_est_civil=%s;', empleado[12])
    id_est_civ_empleado, tipo_est_civ_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.est_civil;'
    cursor.execute(sql)
    est_civiles = cursor.fetchall()

    cursor.execute('SELECT * FROM rrhh.categorias WHERE id_categoria=%s;', empleado[11])
    id_categ_empleado, tipo_categ_empleado = cursor.fetchone()

    sql = 'SELECT * FROM rrhh.categorias;'
    cursor.execute(sql)
    categorias = cursor.fetchall()

    sql = 'SELECT id_localidad, nombre FROM rrhh.localidades WHERE id_localidad=%s;'
    cursor.execute(sql, empleado[14])
    id_local_empleado, nombre_local_empleado = cursor.fetchone()

    sql = 'SELECT id_provincia, nombre FROM rrhh.provincias WHERE id_provincia=%s;'
    cursor.execute(sql, empleado[15])
    id_prov_empleado, nombre_prov_empleado = cursor.fetchone()
    id_loc_prov_empleado = str(id_local_empleado) + '-' + str(id_prov_empleado)
    lyp_completo_empleado = nombre_local_empleado + ' - ' + nombre_prov_empleado

    sql = '''SELECT 
                CONCAT(loc.id_localidad,'-',prov.id_provincia) AS loc_prov,
                CONCAT(loc.nombre, ' - ', prov.nombre) AS lyp_completo  
                FROM rrhh.localidades AS loc
                JOIN rrhh.provincias AS prov
                WHERE loc.id_provincia = prov.id_provincia
                ORDER BY lyp_completo;'''
    cursor.execute(sql)
    locs_y_provs = cursor.fetchall()

    return render_template('rrhh/edit.html',
        empleado=empleado,
        id_doc_empleado=id_doc_empleado,
        tipo_doc_empleado=tipo_doc_empleado,
        documentos=tipo_docs,
        id_est_civ_empleado=id_est_civ_empleado,
        tipo_est_civ_empleado=tipo_est_civ_empleado,
        est_civiles=est_civiles,
        id_categ_empleado=id_categ_empleado,
        tipo_categ_empleado=tipo_categ_empleado,
        categorias=categorias,
        id_loc_prov_empleado=id_loc_prov_empleado,
        lyp_completo_empleado=lyp_completo_empleado,
        locs_y_provs=locs_y_provs,
        )


# PARA CONFIRMAR LA ELIMINACION DE UN EMPLEADO
@app.route('/borrar/<int:id_empleado>')
def borrar(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''SELECT id_empleado, foto, apellidos, nombres 
                FROM rrhh.personal 
                WHERE id_empleado=%s;'''
    cursor.execute(sql, id_empleado)
    empleado = cursor.fetchone()

    conn.close()

    return render_template('rrhh/borrar.html', empleado=empleado)


# PARA ELIMINAR DEFINITIVAMENTE AL EMPLEADO SELECCIONADO
@app.route('/destroy', methods=['POST'])
def destroy():
    id_empleado = request.form['txtIdEmpleado']

    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT foto FROM rrhh.personal WHERE id_empleado=%s;'
    cursor.execute(query, id_empleado)
    registro = cursor.fetchone()
    os.remove(MY_PATH + '/uploads/' + registro[0])
    cursor.execute('DELETE FROM rrhh.personal WHERE id_empleado=%s', (id_empleado))

    conn.commit()
    conn.close()
    return redirect('/')


# PARA DECIDIR SOBRE LICENCIAS DE UN EMPLEADO
@app.route('/licencia/<int:id_empleado>')
def licencia(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''SELECT id_empleado, apellidos, nombres,
                fecha_ingreso, saldo_licencia, licencia_curso, fecha_regreso 
                FROM rrhh.personal 
                WHERE id_empleado=%s;'''
    cursor.execute(sql, id_empleado)
    empleado = cursor.fetchone()

    sql = '''SELECT lg.id_legajo, lg.fecha_desde, lg.fecha_hasta, ev.descripcion, lg.cantidad
            FROM
                rrhh.legajos AS lg
                    JOIN
                rrhh.eventos AS ev
            WHERE
                lg.id_empleado = %s
                    AND lg.cd_evento = ev.cd_evento
            ORDER BY fecha_desde DESC;'''
    cursor.execute(sql, id_empleado)
    legajos = cursor.fetchall()

    conn.close()

    return render_template('rrhh/mnu_licencias.html', empleado=empleado, legajos=legajos)


# PARA INGRESAR UNA LICENCIA A UN EMPLEADO
@app.route('/ing_licencias/<int:id_empleado>')
def ing_licencias(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = 'SELECT id_evento, descripcion FROM rrhh.eventos;'
    cursor.execute(sql)
    eventos = cursor.fetchall()

    sql = '''SELECT id_empleado, apellidos, nombres,
                fecha_ingreso, saldo_licencia, licencia_curso, fecha_regreso 
                FROM rrhh.personal 
                WHERE id_empleado=%s;'''
    cursor.execute(sql, id_empleado)
    empleado = cursor.fetchone()

    conn.close()

    return render_template('rrhh/ing_licencias.html', empleado=empleado, eventos=eventos)


# PARA INGRESAR LAS FECHAS DE LA LICENCIA
@app.route('/updlicencia', methods=['POST'])
def updlicencia():
    id_empleado = request.form['txtIdEmpleado']
    fecha_inicio = request.form['dateFechaInicio']
    fecha_fin = request.form['dateFechaFin']
    licencia_curso = request.form['txtLicenciaEnCurso']
    saldo_licencia = request.form['txtSaldoLicEnCurso']
    afecta_licencia = bool(request.form['rdoSiAfectaNo'])
    fecha_regreso = request.form['txtFechaRegreso']
    id_evento = request.form['txtIdEvento']
    fecha_ingreso = request.form['txtFechaIngreso']
    imprime_planilla = bool(request.form['chbxImprimePlanilla'])

    if fecha_fin == '' or fecha_inicio == '':
        flash('Faltan datos obligatorios!')
        return redirect(url_for('licencia', id_empleado=id_empleado))

    if cl.stod(fecha_inicio) > cl.stod(fecha_fin):
        flash('La fecha de inicio no puede ser mayor a la fecha de fin!')
        return redirect(url_for('licencia', id_empleado=id_empleado))

    if cl.stod(fecha_inicio) < cl.stod(fecha_regreso):
        flash('Para la fecha de inicio ingresada el empleado todavía está en licencia anterior!')
        return redirect(url_for('licencia', id_empleado=id_empleado))

    nva_licen_curso, nvo_saldo_lic, nva_fecha_fin, nva_fecha_regreso, cant_dias, se_paso = cl.calc_lic_en_curso(id_empleado,
                                                                                                'lic',
                                                                                                fecha_ingreso,
                                                                                                fecha_inicio,
                                                                                                fecha_fin,
                                                                                                licencia_curso,
                                                                                                saldo_licencia,
                                                                                                fecha_regreso,
                                                                                                afecta_licencia)
    fecha_inicio = cl.stod(fecha_inicio)
    fecha_ingreso = cl.stod(fecha_ingreso)

    conn = mysql.connect()
    cursor = conn.cursor()

    # TRAIGO LOS DATOS ANTERIORES ANTES DE ACTUALIZAR LOS VALORES DE LA LICENCIA
    sql = '''SELECT apellidos, nombres, saldo_licencia, licencia_curso
                FROM rrhh.personal 
                WHERE id_empleado=%s;'''
    cursor.execute(sql, id_empleado)
    empleado = cursor.fetchone()

    # ACTUALIZO LOS DATOS DE LA LICENCIA
    sql = '''UPDATE rrhh.personal
            SET saldo_licencia=%s, licencia_curso=%s, fecha_regreso=%s
            WHERE id_empleado=%s;
            '''.format(nvo_saldo_lic, nva_licen_curso, nva_fecha_regreso, id_empleado)
    datos = (nvo_saldo_lic, nva_licen_curso, nva_fecha_regreso, id_empleado)
    cursor.execute(sql, datos)
    
    # INSERTO EL REGISTRO DE LA LICENCIA EN LA TABLA DE LEGAJOS
    sql = '''INSERT INTO rrhh.legajos(id_empleado, fecha_desde, fecha_hasta, cd_evento, cantidad)
            VALUES (%s,%s,%s,%s,%s);
            '''.format(id_empleado, fecha_inicio, nva_fecha_fin , id_evento, cant_dias)
    datos = (id_empleado, fecha_inicio, nva_fecha_fin, id_evento, cant_dias)
    cursor.execute(sql, datos)
    conn.commit()

    # OBTENGO EL DETALLE DEL TIPO DE LICENCIA DESDE LA TABLA DE EVENTOS
    sql = 'SELECT descripcion FROM rrhh.eventos WHERE id_evento=%s;'
    cursor.execute(sql, id_evento)
    tipo_licencia = cursor.fetchone()

    conn.close()
   
    if imprime_planilla:
        # ----------------------------------------------------------------------------------
        # PARA IMPRIMIR LA LICENCIA
        # ----------------------------------------------------------------------------------
        planilla = ''
        for i in range (1,3):
            planilla += '    EL FIDEO FELIZ de Jose F. Pes\n'
            planilla += '    Perito Moreno 276, Rawson.(CH) - Tel/Fax (0280) 448-2993 448-5516\n'
            planilla += '    fideofelizrw@gmail.com\n'
            planilla += '    ---------------------------------------------------------------------------\n\n'
            planilla +=f'        PLANILLA DE LICENCIA          ({tipo_licencia[0]})\n'
            planilla +=f'        ====================                           Rawson, CH. {(dt.date.today()).strftime("%d/%m/%Y")}\n\n'

            if i == 1:
                planilla += '      Por intermedio de la presente le solicito a Usted que mi próximo goce\n'
            else:
                planilla += '      Por intermedio de la presente le comunicamos a Ud. que el goce vacacional \n      solicitado, correspondiente al año '

            if i == 2:
                if se_paso: # si se pasó de año
                    planilla += str(nva_licen_curso - 1) + ' / ' + str(nva_licen_curso)
                else: # no se pasó de año
                    planilla += str(nva_licen_curso)

            if i == 1:
                planilla += f'      vacacional me sea otorgado desde el día {fecha_inicio.strftime("%d/%m/%Y")} y hasta el día\n      '
            else:
                planilla += f', le ha sido otorgado desde el día\n      {fecha_inicio.strftime("%d/%m/%Y")} y hasta el día '

            planilla += f'{nva_fecha_fin.strftime("%d/%m/%Y")}, '

            if i == 1:
                planilla += 'asumiendo la responsabilidad de reintegrarme el día '
            else:
                planilla += 'debiendose reintegrar el día\n'

            if i == 1:
                planilla += f'{nva_fecha_regreso.strftime("%d/%m/%Y")}\n      a mi primera obligación.\n'
            else:
                planilla += f'      {nva_fecha_regreso.strftime("%d/%m/%Y")} a su primera obligación.\n'

            if i == 1:
                planilla += '\n\n\n\n'
            else:
                planilla += '\n      Sirva la presente de instrumento de notificación fehaciente.\n\n\n\n\n'

            if i == 1:
                planilla += '         ............................\n'
                planilla += f'            {empleado[0]}, {empleado[1]}\n'
                planilla += '                Dependiente\n\n\n'
            else:
                planilla += '         ............................\n\n'
                planilla += '               p/EL FIDEO FELIZ\n\n\n'

            if afecta_licencia:
                vie_dias_lic = cl.dias_d_lic(fecha_ingreso, fecha_inicio)

                if se_paso:
                    resto = abs(vie_dias_lic - cant_dias)
                    dias_lic = vie_dias_lic - resto

                    reng1 = f'    {str(empleado[2])} dias de {str(vie_dias_lic)} / Licencia {str(empleado[3])}\n'
                    reng1 += f'    {str(resto)} dias de {str(dias_lic)} / Licencia {str(nva_licen_curso)}'
                else:
                    tomados = vie_dias_lic - empleado[2]

                    reng1 = f'''    {(tomados + cant_dias)} dias de {str(vie_dias_lic)} / Licencia {str(nva_licen_curso)}'''
            else:
                reng1 = ' '

            if i == 1:
                planilla += '\n\n\n\n'
            else:
                planilla += reng1

        filename = tempfile.mktemp(".txt")
        open(filename, "w").write(planilla)
        win32api.ShellExecute(0, "printto", filename, '"%s"' % win32print.GetDefaultPrinter(), ".", 0)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
