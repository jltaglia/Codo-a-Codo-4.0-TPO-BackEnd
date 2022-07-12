from flask import Flask, flash
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
import calcula_licencia as cl


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

    return render_template('rrhh/create.html', documentos=tipo_docs, est_civiles=est_civiles, categorias=categorias, locs_y_provs=locs_y_provs)


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
    datos = (apellidos, nombres, id_tipo_doc, nro_doc, cuil, fecha_nac, fch_ingreso, id_categoria, id_est_civil, domicilio, id_localidad, id_provincia, tel, mail)
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
        img.save('C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/TPO Back/uploads/' + nuevo_nombre_img)
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


# PARA ELIMINAR UN EMPLEADO
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


# PARA EDITAR LOS DATOS DE UN EMPLEADO
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM netflax_22085.peliculas WHERE id=%s', (id))
    peli = cursor.fetchone()

    return render_template('peliculas/edit.html', peli=peli)


if __name__ == '__main__':
    app.run(debug=True)
