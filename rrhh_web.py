from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime


rrhh_web = Flask(__name__)

mysql = MySQL()
rrhh_web.config['MYSQL_DATABASE_HOST'] = 'localhost'
rrhh_web.config['MYSQL_DATABASE_USER'] = 'root'
rrhh_web.config['MYSQL_DATABASE_PASSWORD'] = ''
rrhh_web.config['MYSQL_DATABASE_DB'] = 'rrhh'
mysql.init_app(rrhh_web)

@rrhh_web.route('/')
def index():
    sql ="SELECT * FROM rrhh.empleados"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    return render_template('index.html', empleados=empleados)

# @rrhh_web.route('/create')
# def create():
#     return render_template('peliculas/create.html')

# @rrhh_web.route('/store', methods=['POST'])
# def storage():
#     nombre = request.form['txtNombre']
#     desc = request.form['txtDesc']
#     img = request.files['txtImagen']
#     now = datetime.now()
#     tiempo = now.strftime("%Y%H%M%S")
#     if img.filename != '':
#         nuevo_nombre_img = tiempo + img.filename
#         img.save("C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022/Material de Clase/10- FLASK/netflax_22085/uploads/" + nuevo_nombre_img)

#     sql ="INSERT INTO netflax_22085.peliculas (nombre, descripcion, imagen) VALUES (%s, %s, %s)".format(nombre, desc, img)
#     datos = (nombre, desc, nuevo_nombre_img)
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute(sql, datos)
#     conn.commit()
#     return redirect('/')

# @rrhh_web.route('/destroy/<int:id>')
# def destroy(id):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM netflax_22085.peliculas WHERE  id=%s", (id))
#     conn.commit()
#     return redirect('/')

# @rrhh_web.route('/edit/<int:id>')
# def edit(id):
#     conn = mysql.connect()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM netflax_22085.peliculas WHERE id=%s", (id))
#     peli = cursor.fetchone()

#     return render_template('peliculas/edit.html', peli=peli)


if __name__ == '__main__':
    rrhh_web.run(debug=True)


