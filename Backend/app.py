from flask import Flask, jsonify, request
from flask_cors import CORS # para permitir el acceso a la API desde el frontend
import pymysql
import bcrypt # incriptar contrasena
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
Swagger = Swagger(app)

#conexion a la base de datos
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.Connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para consulta general
@app.route("/", methods=['GET'])
def consulta_general():

    try:
        conn = conectar('localhost', 'root', 'Es1084734914', 'gestor_contrasena') # conexion a la base de datos
        cur = conn.cursor() # cursor para ejecutar consultas
        cur.execute("SELECT * FROM baul") # consulta a la base de datos
        datos = cur.fetchall() # obtener todos los registros
        data = []
        for  row in datos:
            dato = {'id_baul':row[0], 'plataforma': row[1], 'usuario': row[2], 'clave': row[3]} # crear un diccionario con los datos
            data.append(dato) # agregar a la lista
        cur.close() # cerrar el cursor
        conn.close() # cerrar la conexion
        return jsonify({'baul': data, 'mesaje': 'Baul de contrasena'})
    except Exception as ex:
        print(ex) # imprimir el error
        return jsonify ({'mesaje':'Error'}) # devolver un mensaje de error
    
    # Ruta para consulta individual
@app.route("/consulta_individual/<codigo>", methods=['GET'])  
def consulta_individual(codigo):  # codigo es el id del registro
    """
    Consulta individual por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro encontrado
    """ 

    try: 
        conn = conectar('localhost', 'root', 'Es1084734914', 'gestor_contrasena')
        cur = conn.cursor() # cursor para ejecutar consultas
        cur.execute(f"SELECT * FROM baul WHERE id_baul = '{codigo}'") # consulta a la base de datos
        datos = cur.fetchone() # obtener un solo registro
        cur.close() # cerrar el cursor
        conn.close() # cerrar la conexion
        # verificar si se encontro el registro
        if datos:
            # crear un diccionario con los datos
            dato = {'id_baul': datos[0], 'Plataforma': datos[1], 'usuario': datos[2], 'clave': datos[3]}
            return jsonify ({'baul': dato, 'mesaje': 'Registro encontrado'})
        # si no se encontro el registro
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
        # cerrar el cursor
    except Exception as ex:
        # imprimir el error
        print(ex)
        return jsonify({'mesaje': 'Error'}) # devolver un mensaje de error  
    

# Ruta de registro
@app.route("/registro/", methods=['POST'])
def registro():
    """
    Registra nueva contraseña
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: Registro agregado
    """
    try: 
        data = request.get_json()
        plataforma = data ['plataforma']
        usuario = data['usuario']
        clave = bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = conectar('localhost', 'root', 'Es1084734914', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)",
                    (plataforma, usuario, clave))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})
    
    # Ruta para eliminar registro
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    Eliminar registro por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Registro eliminado
    """
    try:
        conn = conectar('localhost', 'root', 'Es1084734914', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mesaje': 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mesaje': 'Error'})
    
    # Ruta para  actualizar registro
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Actualizar registro por ID
    ---
    parameters:
      - name: codigo
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            plataforma:
              type: string
            usuario:
              type: string
            clave:
              type: string
    responses:
      200:
        description: Registro actualizado
    """
    try:
        data = request.get_json()
        plataforma = data['plataforma']
        usuario = data['usuario']
        clave =bcrypt.hashpw(data['clave'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = conectar('localhost', 'root', 'Es1084734914', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul =%s",
                    (plataforma, usuario, clave, codigo))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mesaje': 'Error'})
        
if __name__ =='__main__':
    app.run(debug=True)
      