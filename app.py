from flask import Flask, render_template, request, flash, redirect
from flask_mysqldb import MySQL
from datetime import date
today = date.today()
app = Flask(__name__)
app.secret_key = 'my unobvious secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'inventory_system'

mysql = MySQL(app)

@app.route('/index')
def index():
    DateOrdered = today.strftime("%m/%d/%y")

    awpfetch = mysql.connection.cursor()
    awpfetch.execute("select count(id) from rack_1 where status = 'AWP';")
    awpfetch = awpfetch.fetchone()
    
    ipfetch = mysql.connection.cursor()
    ipfetch.execute("select count(id) from rack_1 where status = 'IP';")
    ipfetch = ipfetch.fetchone()

    repairedfetch = mysql.connection.cursor()
    repairedfetch.execute("select count(id) from rack_1 where status = 'Repaired';")
    repairedfetch = repairedfetch.fetchone()
    
    return render_template("index.html", awpfetch=awpfetch[0], ipfetch=ipfetch[0], repairedfetch=repairedfetch[0], DateOrdered=DateOrdered)
    

@app.route('/checkin')
def form():
    return render_template('checkin.html')

@app.route('/awpin', methods = ['POST'])
def login():

        ServiceOrder = request.form['ServiceOrder']
        PartType = request.form['PartType']
        SKU = request.form['SKU']
        Model = request.form['Model']
        Cart = request.form['Cart']
        DateOrdered = today.strftime("%m/%d/%y")
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO rack_1 (ServiceOrder, SKU, Model, Cart, DateOrdered, PartType) VALUES(%s,%s,%s,%s,%s,%s)''',(ServiceOrder,SKU,Model,Cart,DateOrdered,PartType))
        mysql.connection.commit()
        cursor.close()
        flash(ServiceOrder)
        return render_template('checkin.html')

@app.route("/awp", methods=['GET'])
def awptable():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rack_1 where status = 'AWP' order by id desc;")
    data = cursor.fetchall()
    return render_template("awptable.html", data=data)

@app.route('/status')
def status():
    
    return render_template('status.html')

@app.route("/statuspost", methods=['POST'])
def statuspost():

    RepairID = request.form['RepairID']
    StatusChange = request.form['statuschange']
    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE rack_1 SET Status = %s WHERE id = %s''',(StatusChange, RepairID))
    mysql.connection.commit()
    cursor.close()
    return render_template("status.html")

@app.route("/ip", methods=['GET'])
def iptable():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rack_1 where status = 'IP' order by id desc;")
    data = cursor.fetchall()
    return render_template("iptable.html", data=data)

@app.route("/ippost", methods=['POST'])
def ippost():

    change_to_ip = request.form['change_to_ip']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE rack_1 SET Status = 'IP' WHERE id = %s",[change_to_ip])
    mysql.connection.commit()
    cursor.close()
    return redirect(request.referrer)


@app.route("/repaired", methods=['GET'])
def repairedtable():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rack_1 where status = 'Repaired' order by DateOrdered desc;")
    data = cursor.fetchall()
    return render_template("repairedtable.html", data=data)

@app.route("/repairedpost", methods=['POST'])
def repairedpost():
    DateOrdered = today.strftime("%m/%d/%y")
    change_to_repaired = request.form['change_to_repaired']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE rack_1 SET Status = 'Repaired', Checkout= %s WHERE id = %s",[DateOrdered,change_to_repaired])
    mysql.connection.commit()
    cursor.close()
    return redirect(request.referrer)

app.run(debug=True)
app.run(host='localhost', port=5000)
