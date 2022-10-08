import mysql.connector as mysql
from mysql.connector import Error
import time

# DATABASE PARAMETERS
DB_NAME = 'rrhh'
DB_USER = 'root'
DB_PASSWORD = 'pep45051'

empieza = time.strftime("%m/%d/%Y, %H:%M:%S")

try:
    conn = mysql.connect(host='localhost', database=DB_NAME, user=DB_USER , password=DB_PASSWORD)
    if conn.is_connected():
        cursor = conn.cursor()
        
        sql = '''SELECT id_legajo, id_empleado, id_evento, cd_evento
            FROM rrhh.legajos 
            ORDER BY cd_evento;'''
        cursor.execute(sql)
        legajos = cursor.fetchall()

        sql = '''SELECT id_evento, cd_evento
            FROM rrhh.eventos 
            ORDER BY cd_evento;'''
        cursor.execute(sql)
        eventos = cursor.fetchall()

        print(eventos)
        
        for legajo in legajos:
            id_event = [evento[0] for evento in eventos if evento[1] == legajo[3]]
            sql = '''UPDATE rrhh.legajos 
                    SET id_evento=%s WHERE id_legajo=%s;
                    '''.format(id_event[0], legajo[0])
            datos = (id_event[0], legajo[0])
            cursor.execute(sql, datos)
        # the connection is not auto committed by default, so we must commit to save our changes
        conn.commit()
        conn.close()

except Error as e:
            print("Error while connecting to MySQL", e)

termina = time.strftime("%m/%d/%Y, %H:%M:%S")

print(f'\n\nBeggining: {empieza}')
print(f'End: {termina}')