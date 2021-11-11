import mysql.connector 
mydb = mysql.connector.connect(
            host='localhost',
            user='yiyanw3',
            database='yiyanw3_database',
            password='!1234QWERasdf')
mycursor = mydb.cursor() 

mycursor.execute("create asd dfg")