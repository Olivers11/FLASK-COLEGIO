from flask import *
from flask_mysqldb import MySQL
#import time



app  = Flask(__name__)

#   CONFIGURATION 
#-----------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'base1'
#--------INSTANCICA------------
app.secret_key = 'mysecretkey'
#------------------------------
mysql = MySQL(app)
#------------------------------

@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/eliminar/<id>')
def Delete(id):
    cur = mysql.connection.cursor()
    sql = "delete from profesor where Nombre = '{}'".format(id)
    cur.execute(sql)
    mysql.connection.commit()
    flash("Eliminado Correctamente")
    return redirect(url_for('Principal'))



@app.route('/Principal')
def Principal():
    cur = mysql.connection.cursor()
    cur.execute("select * from profesor")
    data = cur.fetchall()
    print(data)
    return render_template('Principal.html', contacts=data)

@app.route('/Insertar')
def Insert():
    return render_template('insert.html')

@app.route('/edit/<id>')
def Editar(id):
    cur = mysql.connection.cursor()
    sql = "select * from profesor where Nombre = '{}'".format(id)
    cur.execute(sql)
    dato = cur.fetchall()
    return render_template('editar.html', contact=dato[0])


@app.route('/update/<id>', methods=['POST'])
def Actualizar(id):
    if request.method == 'POST':
        name = request.form['Nombre']
        age = request.form['Edad']
        document = request.form['DPI']
        title = request.form['Titulo']
        number = request.form['NIT']
        salud = request.form['IG']
        work = request.form['Años']
        sql = "update profesor set Nombre = %s, Edad = %s, DPI = %s, Titulo = %s, Labor = %s, NIT = %s, IGSS = %s where Nombre = %s"
        cur = mysql.connection.cursor()
        cur.execute(sql,(name, age, document, title, work, number, salud, id))
        mysql.connection.commit()
        #flash('Profesor ' + str(name) + ' editado correctamente')
        return redirect(url_for('Principal'))


@app.route('/Save', methods=['POST'])
def Save_Docent():
    if request.method == 'POST':
        name = request.form['Nombre']
        age = request.form['Edad']
        document = request.form['DPI']
        title = request.form['Titulo']
        number = request.form['NIT']
        salud = request.form['IG']
        work = request.form['Años']
        cur = mysql.connection.cursor()
        sql = 'insert into profesor(Nombre, Edad, DPI, Titulo, Labor, NIT, IGSS)values(%s, %s, %s, %s, %s, %s,%s)'
        cur.execute(sql, (name, age, document, title, work, number, salud))
        mysql.connection.commit()
        #flash("Ingresado Correctamente ")
        return redirect(url_for('Principal'))





@app.route('/login', methods=['POST'])
def Login():
    if request.method == 'POST':
        name = request.form['Nombre']
        contra = request.form['Contraseña']
        #password = request.form['Contraseña']
        sql = "select * from colegio where Nombre = '{}' and Contraseña = '{}'".format(name, contra)
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        #print(contra)
        account = cursor.fetchone()
        if account:
            flash('Bienvenido ' + str(name))
            return redirect(url_for('Principal'))
            #time.sleep(3)
        else:
            flash('Contraseña Incorrecta')
            return redirect(url_for('Index'))



if __name__ == '__main__':
    app.run(port=3000, debug=True)







