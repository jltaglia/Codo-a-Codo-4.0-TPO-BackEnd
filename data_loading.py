import mysql.connector as mysql
from mysql.connector import Error
from pprint import pprint
import pandas as pd
import time

# DATABASE PARAMETERS
DB_NAME = 'test'
DB_USER = 'root'
DB_PASSWORD = ''

# LIST OF TABLES TO IMPORT
TABLES = ['categorias', 'est_civil', 'eventos', 'legajos', 'localidades', 'parentescos', 'personal', 'provincias', 'tipo_doc']

empieza = time.strftime("%m/%d/%Y, %H:%M:%S")

for table in TABLES:
    empdata = pd.read_csv(f'./csv/{table}.csv', index_col=False, delimiter = ';', encoding='latin-1')
    print('----------------------------------------------------------')

    try:
        conn = mysql.connect(host='localhost', database=DB_NAME, user=DB_USER , password=DB_PASSWORD)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record[0], 'tabla:', table)
            #loop through the data frame
            for i,row in empdata.iterrows():
                #here %S means string values
                param = ''
                for c in range(len(row)):
                    param += f'%s,'
                param = param[:-1]
                sql = f"INSERT INTO {DB_NAME}.{table} VALUES ({param})"
                cursor.execute(sql, tuple(row))
                print("Record inserted:",i,'\b\b')

            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
            conn.close()

    except Error as e:
                print("Error while connecting to MySQL", e)

termina = time.strftime("%m/%d/%Y, %H:%M:%S")

print(f'\n\nBeggining: {empieza}')
print(f'End: {termina}')