from flask import Flask, render_template, request, abort
import mysql.connector
import re
app = Flask(__name__) 

mydb = mysql.connector.connect(
            host='localhost',
            user='yiyanw3',
            database='yiyanw3_database',
            password='!1234QWERasdf')

@app.route('/', methods=['GET'])
def loginPage():
    return render_template('enroll.html', result=None)

# http://20.88.14.242:10056/delete query_string drop table Test
@app.route("/delete", methods = ['POST'])
def deleteSth():
    sql = request.form['query_string']
    if sql.split()[0].upper() != "DELETE" and sql.split()[0].upper() != "DROP":
        abort(400, "must be create")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
        mydb.commit()
    except:
        abort(400, "fail to create table") 

    return 'success'

# postman: http://20.88.14.242:10056/create  key:query_string value:create table acc ( number   char(3))
@app.route("/create", methods = ['POST'])
def newTable():
    sql = request.form['query_string']
    if sql.split()[0].upper() != "CREATE":
        abort(400, "must be create")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
        mydb.commit()
    except:
        abort(400, "fail to create table") 

    return 'success'

# http://20.88.14.242:10056/insert key:query_string value:insert into account values (101, 'J. Smith', 1000.00, 'checking')
@app.route("/insert", methods = ['POST'])
def insertRecord():
    sql = request.form['query_string']
    print(sql)
    if sql.split()[0].upper() != "INSERT":
        abort(400, "must be insert")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        mycursor.execute(sql)
        mydb.commit()
    except:
        abort(400, "fail to insert record") 

    return 'success'


@app.route("/update", methods = ['POST'])
def updateRecord():
    sql = request.form['query_string']
    print(sql)
    
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
    except:
        abort(400, "fail to update") 

    return 'success'

# http://20.88.14.242:10056/select key:query_string values:select * from account
@app.route("/select", methods = ['POST'])
def showRecord():
    sql = request.form['query_string']
    
    if sql.split()[0].upper() != "SELECT":
        abort(400, "must be select")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record") 

    # print([type(row[0]) for row in mycursor.description]) 
    # print([row for row in mycursor])
    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    # print([type(row) for row in mycursor])
    result['data']['values'] = [row for row in mycursor]
    return result


if __name__ == '__main__':
    app.run('0.0.0.0', 10058, False)

