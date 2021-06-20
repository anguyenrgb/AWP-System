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
    awpfetch.execute("select count(id) from inventory where status = 'AWP';")
    awpfetch = awpfetch.fetchone()
    
    ipfetch = mysql.connection.cursor()
    ipfetch.execute("select count(id) from inventory where status = 'IP';")
    ipfetch = ipfetch.fetchone()

    repairedfetch = mysql.connection.cursor()
    repairedfetch.execute("select count(id) from inventory where status = 'Repaired';")
    repairedfetch = repairedfetch.fetchone()
    
    return render_template("index.html", awpfetch=awpfetch[0], ipfetch=ipfetch[0], repairedfetch=repairedfetch[0], DateOrdered=DateOrdered)
    

@app.route('/checkin')
def form():
    return render_template('checkin.html')

@app.route('/awpin', methods = ['POST'])
def login():

        ServiceOrder = request.form['ServiceOrder']
        UnitSKU = request.form['UnitSKU']
        PartType = request.form['PartType']
        Remarks = request.form['Remarks']
        PartSKU = request.form['SKU']
        Model = request.form['Model']
        Cart = request.form['Cart']
        DateOrdered = today.strftime("%m/%d/%y")
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO inventory (ServiceOrder, UnitSKU, PartType, Remarks, PartSKU, Model, Cart, DateOrdered)
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',[ServiceOrder,UnitSKU,PartType,Remarks,PartSKU,Model,Cart,DateOrdered])
        mysql.connection.commit()
        cursor.close()
        flash(ServiceOrder)
        return render_template('checkin.html')

@app.route("/awp", methods=['GET'])
def awptable():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory where status = 'AWP' order by id desc;")
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
    cursor.execute('''UPDATE inventory SET Status = %s WHERE id = %s''',[StatusChange, RepairID])
    mysql.connection.commit()
    cursor.close()
    return render_template("status.html")

@app.route("/statusdelete", methods=['POST'])
def statusdelete():

    deleteID = request.form['deleteID']
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = %s;",[deleteID])
    mysql.connection.commit()
    cursor.close()
    return render_template("status.html")

@app.route("/ip", methods=['GET'])
def iptable():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory where status = 'IP' order by id desc;")
    data = cursor.fetchall()
    return render_template("iptable.html", data=data)

@app.route("/ippost", methods=['POST'])
def ippost():

    change_to_ip = request.form['change_to_ip']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE inventory SET Status = 'IP' WHERE id = %s;",[change_to_ip])
    mysql.connection.commit()
    cursor.close()
    flash(change_to_ip)
    return redirect(request.referrer)


@app.route("/repaired", methods=['GET'])
def repairedtable():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory where status = 'Repaired' order by Checkout desc;")
    data = cursor.fetchall()
    return render_template("repairedtable.html", data=data)

@app.route("/repairedpost", methods=['POST','GET'])
def repairedpost():
    DateOrdered = today.strftime("%m/%d/%y")
    change_to_repaired = request.form['change_to_repaired']
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE inventory SET Status = 'Repaired', Checkout= %s WHERE id = %s",[DateOrdered,change_to_repaired])
    mysql.connection.commit()
    cursor.close()
    flash(change_to_repaired)
    return redirect(request.referrer)

@app.route('/editpost', methods=['POST','GET'])
def edit():
    editID = request.form['editID']

    idpull = mysql.connection.cursor()
    idpull.execute("select id from inventory where id = %s",[editID])
    idpull = idpull.fetchone()

    servicepull = mysql.connection.cursor()
    servicepull.execute("select ServiceOrder from inventory where id = %s",[editID])
    servicepull = servicepull.fetchone()

    unitskupull = mysql.connection.cursor()
    unitskupull.execute("select UnitSKU from inventory where id = %s",[editID])
    unitskupull = unitskupull.fetchone()

    partpull = mysql.connection.cursor()
    partpull.execute("select PartType from inventory where id = %s",[editID])
    partpull = partpull.fetchone()

    remarkspull = mysql.connection.cursor()
    remarkspull.execute("select Remarks from inventory where id = %s",[editID])
    remarkspull = remarkspull.fetchone()

    skupull = mysql.connection.cursor()
    skupull.execute("select PartSKU from inventory where id = %s",[editID])
    skupull = skupull.fetchone()

    modelpull = mysql.connection.cursor()
    modelpull.execute("select Model from inventory where id = %s",[editID])
    modelpull = modelpull.fetchone()
    
    cartpull = mysql.connection.cursor()
    cartpull.execute("select Cart from inventory where id = %s",[editID])
    cartpull = cartpull.fetchone()
    
    return render_template('edit.html',idpull=idpull[0],servicepull=servicepull[0],unitskupull=unitskupull[0],
    partpull=partpull[0],remarkspull=remarkspull[0],skupull=skupull[0],modelpull=modelpull[0],cartpull=cartpull[0])

@app.route('/updatepost', methods = ['POST'])
def update():
        editID = request.form['editID']
        ServiceOrder = request.form['ServiceOrder']
        UnitSKU = request.form['UnitSKU']
        PartType = request.form['PartType']
        Remarks = request.form['Remarks']
        PartSKU = request.form['SKU']
        Model = request.form['Model']
        Cart = request.form['Cart']
        updaterecord = mysql.connection.cursor()
        updaterecord.execute('''UPDATE inventory set ServiceOrder=%s,UnitSKU=%s,PartType=%s,Remarks=%s,PartSKU=%s,Model=%s,Cart=%s where id = %s''',[ServiceOrder,UnitSKU,PartType,Remarks,PartSKU,Model,Cart,editID])
        mysql.connection.commit()
        updaterecord.close()
        flash(editID)
        return render_template('edit.html')

app.run(debug=True)
app.run(host='localhost', port=5000)
