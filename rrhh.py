from flask import Flask, flash
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
import calcula_licencia as cl
from pprint import pprint


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
        nuevo_nombre_img = str(id_empleado).zfill(3) + '_' + tiempo + img.filename[-4:]
        img.save(MY_PATH + '/uploads/' + nuevo_nombre_img)
        # img.save(os.path.join(app.config['CARPETA'], nuevo_nombre_img))
    # CALCULO LA LICENCIA EN CURSO Y LOS DIAS QUE LE CORRESPONDEN
    licen_curso, saldo_licen = cl.calc_lic_en_curso(id_empleado, 'alta')
    #
    sql = '''UPDATE rrhh.personal 
            SET foto=%s, saldo_licencia=%s, licencia_curso=%s WHERE id_empleado=%s;
            '''.format(nuevo_nombre_img, saldo_licen, licen_curso, id_empleado)
    datos = (nuevo_nombre_img, saldo_licen, licen_curso, id_empleado)
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
       nuevo_nombre_img = str(id_empleado).zfill(3) + '_' + tiempo + img.filename[-4:]
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


# PARA ELIMINAR UN EMPLEADO
@app.route('/destroy/<int:id_empleado>')
def destroy(id_empleado):
    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT foto FROM rrhh.personal WHERE id_empleado=%s;'
    cursor.execute(query, id_empleado)
    registro = cursor.fetchone()
    os.remove(MY_PATH + '/uploads/' + registro[0])
    # os.remove(os.path.join(app.config['CARPETA'], registro[0]))
    cursor.execute('DELETE FROM rrhh.personal WHERE id_empleado=%s', (id_empleado))

    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
