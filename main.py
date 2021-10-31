from flask import Flask, json, jsonify, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
# url del servidor de MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# nombre de usuario
app.config['MYSQL_DATABASE_USER'] = 'root'
# contrasena
app.config['MYSQL_DATABASE_PASSWORD'] = ''
# nombre de base de datos
app.config['MYSQL_DATABASE_DB'] = 'ingreso_universidad'
mysql.init_app(app)
@app.route('/')
def index_route():
 return "Sistema para control de ingreso de la universidad"
@app.route('/estudiante', methods=['GET', 'POST'])
def index_estudiantes():
    if(request.method== 'POST'):
        new_student= request.get_json()
        name=new_student['name']
        lastname=new_student['lastname']
        age=new_student['age']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO Estudiantes(name,lastname,age)VALUES(%s, %s, %s)",(name,lastname,age))
        conn.commit()
        cur.close()
        return jsonify({"response":"Student created exitosamente"}),201
    else:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Estudiantes")
        # arreglo de arreglos con la informacion de la DB
        data_estudiantes = cur.fetchall()
        responseData = []
        for estudiante in data_estudiantes:
            responseData.append(
            {
            "id": estudiante[0],
            "name": estudiante[1],
            "lastname": estudiante[2],
            "edad":estudiante[3]
            }
            )
        cur.close()
        print(responseData)
        return jsonify({"response": responseData}), 200
@app.route('/estudiante/<int:student_id>',methods=['GET','PUT','DELETE'])
def student_id(student_id):
    if(request.method=='PUT'):
        conn = mysql.connect()
        cur = conn.cursor()
        info_actualizar_student=request.get_json()
        name = None
        lastname = None
        age = None
        if (info_actualizar_student != None):
            if("name" in info_actualizar_student):
                name=info_actualizar_student['name']
            if("lastname" in info_actualizar_student):
                lastname = info_actualizar_student['lastname']
            if("age" in info_actualizar_student):
                age= info_actualizar_student['age']
        else:
            return jsonify({"response":"La informacion para actulizar esta incompleta"}),400
        if(name!=None and lastname!=None and age!=None):
            respuesta=cur.execute("UPDATE Estudiantes SET name=%s,lastname=%s,age=%s WHERE id=%s",(name,lastname,age,student_id))
        elif(name!=None and lastname!=None):
            respuesta=cur.execute("UPDATE Estudiantes SET name=%s,lastname=%s WHERE id=%s",(name,lastname,student_id))
        elif(name!=None):
            respuesta=cur.execute("UPDATE Estudiantes SET name=%s WHERE id=%s",(name,student_id))
        elif(lastname!=None):
            respuesta=cur.execute("UPDATE Estudiantes SET lastname=%s WHERE id=%s",(lastname,student_id))
        else:
            return jsonify({"response":"ERROR CON LA INFO"}),400
        conn.commit()
        cur.close()
        return jsonify({"response":"ESTUDIANTE"+str(student_id)+ "actualizado con extito!"}),200
@app.route('/matricula',methods=['POST'])
def matricula():
    if(request.method=='POST'):
        new_matricula=request.get_json()
        student_id=new_matricula['student_id']
        clase=new_matricula['clase']
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO Matricula(studid,clase) VALUES(%s,%s)",(student_id,clase))
        conn.commit()
        cur.close()
        return jsonify({"response":"Matricula created exitosamente"}),201

    


