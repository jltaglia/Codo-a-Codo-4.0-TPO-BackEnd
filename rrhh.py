from flask import Flask, flash
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from pprint import pprint

app = Flask(__name__)
app.secret_key = 'Clave'

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'rrhh'
mysql.init_app(app)

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

    sql = '''SELECT loc.id_localidad, prov.id_provincia, CONCAT(loc.nombre, ' - ', prov.nombre) AS lyp_completo
                FROM rrhh.localidades AS loc
                JOIN rrhh.provincias AS prov
                WHERE loc.id_provincia = prov.id_provincia
                ORDER BY lyp_completo;'''
    cursor.execute(sql)
    locs_y_provs = cursor.fetchall()
    conn.close()

    return render_template('rrhh/create.html', documentos=tipo_docs, est_civiles=est_civiles, categorias=categorias, locs_y_provs=locs_y_provs)


@app.route('/store', methods=['POST'])
def storage():
    img = request.files['txtImagen']
    apellidos = request.form['txtApellidos']
    nombres = request.form['txtNombres']
    dni = request.form['TipoDocDataList']
    nro_doc = request.form['txtDoc']
    cuil = request.form['txtCuil']
    fecha_nac = request.form['dateNacim']
    est_civil = request.form['EstCivilDataList']
    fch_ingreso = request.form['dateIngreso']
    categoria = request.form['CategDataList']
    domicilio = request.form['txtDomicilio']
    loc_y_prov = request.form['LocalidadDataList']
    localidad, provincia = loc_y_prov.split(' - ')
    tel = request.form['txtTel']
    mail = request.form['txtEmail']

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = 'SELECT id_documento FROM rrhh.tipo_doc WHERE descripcion=%s;'
    cursor.execute(sql, dni)
    tipo_docs = cursor.fetchone()
    id_tipo_doc = tipo_docs[0]

    sql = 'SELECT id_est_civil FROM rrhh.est_civil WHERE descripcion=%s;'
    cursor.execute(sql, est_civil)
    est_civiles = cursor.fetchone()
    id_est_civil = est_civiles[0]

    sql = 'SELECT id_categoria FROM rrhh.categorias WHERE descripcion=%s;'
    cursor.execute(sql, categoria)
    categorias = cursor.fetchone()
    id_categoria = categorias[0]

    sql = 'SELECT id_provincia FROM rrhh.provincias WHERE nombre = %s;'
    cursor.execute(sql, provincia)
    id_provincia = cursor.fetchone()
    id_provincia = id_provincia[0]

    sql = '''SELECT id_localidad FROM rrhh.localidades 
                WHERE nombre = %s AND id_provincia = %s;'''.format(
        localidad, id_provincia)
    datos = (localidad, id_provincia)
    cursor.execute(sql, datos)
    id_localidad = cursor.fetchone()
    id_localidad = id_localidad[0]


    print(img.filename,'\n', apellidos,'\n', nombres,'\n', id_tipo_doc,'\n', nro_doc,'\n', cuil,'\n', fecha_nac,'\n', id_est_civil,'\n', fch_ingreso,'\n', id_categoria,'\n', domicilio,'\n', id_localidad,'\n', id_provincia,'\n', tel,'\n', mail)
    print('---------------------------------------------------------')
    input('Presione Enter para continuar...')


    if img.filename == '' or apellidos == '' or nombres == '' or id_tipo_doc == '' or nro_doc == '' or cuil == '' or fecha_nac == '' or id_est_civil == '' or fch_ingreso == '' or id_categoria == '' or domicilio == '' or id_localidad == '' or id_provincia == '':
        flash('Faltan datos obligatorios!')
        return redirect(url_for('create'))


    sql = 'SELECT MAX(id_empleado) AS ultimo_id FROM rrhh.personal;'
    cursor.execute(sql)
    ultimo_empleado = cursor.fetchone()
    prox_empleado = int(ultimo_empleado[0]) + 1

    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')
    if img.filename != '':
        nuevo_nombre_img = str(prox_empleado) + tiempo
        img.save('C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/TPO Back/uploads/' + nuevo_nombre_img)
        # img.save(os.path.join(app.config['CARPETA'], nuevo_nombre_img))

    sql = '''INSERT INTO rrhh.personal
            (foto, apellidos, nombres, id_documento, documento,
             cuil, fecha_nacimiento, fch_ingreso, id_categoria,
             id_est_civil, domicilio, id_localidad, id_provincia,
             tel, email, saldo_licencia, licencia_curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''.format(nuevo_nombre_img, nombres, apellidos, id_tipo_doc, nro_doc, cuil, fecha_nac, id_est_civil, fch_ingreso, id_categoria, domicilio, id_localidad, id_provincia, tel, mail, saldo_licen, licen_curso)
    datos = (nuevo_nombre_img, nombres, apellidos, id_tipo_doc, nro_doc, cuil, fecha_nac, id_est_civil, fch_ingreso, id_categoria, domicilio, id_localidad, id_provincia, tel, mail, saldo_licen, licen_curso)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    conn.close()
    return redirect('/')


# PARA MODIFICAR LOS DATOS DE UN EMPLEADO
@app.route('/update', methods=['POST'])
def update():
    nombre = request.form['txtNombre']
    desc = request.form['txtDesc']
    img = request.files['txtImagen']
    id = request.form['txtID']
    now = datetime.now()
    tiempo = now.strftime('%Y%H%M%S')

    if img.filename != '':
        nuevo_nombre_img = tiempo + img.filename
        img.save('C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/Material de Clase/10- FLASK/netflax_22085/uploads/' + nuevo_nombre_img)
        #img.save(os.path.join(app.config['CARPETA'], nuevo_nombre_img))

    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT imagen FROM netflax_22085.peliculas WHERE id=%s;'
    cursor.execute(query, id)
    registro = cursor.fetchone()
    os.remove(
        'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/Material de Clase/10- FLASK/netflax_22085/uploads/' + registro[0])
    # os.remove(os.path.join(app.config['CARPETA'], registro[0]))

    sql = 'UPDATE netflax_22085.peliculas SET nombre=%s, descripcion=%s, imagen=%s WHERE id=%s;'.format(
        nombre, desc, nuevo_nombre_img, id)
    datos = (nombre, desc, nuevo_nombre_img, id)
    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')


@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    query = 'SELECT imagen FROM netflax_22085.peliculas WHERE id=%s;'
    cursor.execute(query, id)
    registro = cursor.fetchone()
    os.remove(
        'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/Material de Clase/10- FLASK/netflax_22085/uploads/' + registro[0])
    # os.remove(os.path.join(app.config['CARPETA'], registro[0]))
    cursor.execute('DELETE FROM netflax_22085.peliculas WHERE  id=%s', (id))

    conn.commit()
    return redirect('/')


@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM netflax_22085.peliculas WHERE id=%s', (id))
    peli = cursor.fetchone()

    return render_template('peliculas/edit.html', peli=peli)


if __name__ == '__main__':
    app.run(debug=True)
