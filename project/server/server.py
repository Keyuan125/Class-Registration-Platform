from flask import Flask, render_template, request, abort
import mysql.connector
import re
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from utility.key_word_search import key_word_search
from utility.prereq import prerequisite


app = Flask(__name__) 

mydb = mysql.connector.connect(
            host='localhost',
            user='yiyanw3',
            database='yiyanw3_database',
            password='!1234QWERasdf')


@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route('/', methods=['GET'])
def mainPage():
    return render_template('easy_hard.html', search=None, enrollment=None)



@app.route("/easy", methods = ['GET', 'POST'])
def easy():
    sql = "select C.CRN, C.Subject, C.Number, C.Name, MAX(avgGPA) \
            from CoursesNew C INNER JOIN GPAsNew G on C.Subject = \
            G.CourseSubject and C.Number = G.CourseNumber WHERE \
            C.Subject = 'CS' GROUP BY C.CRN, C.Subject, C.Number, C.Name HAVING MAX(avgGPA) > 3.8;"
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record")

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    # print([type(row) for row in mycursor])
    result['data']['values'] = [row for row in mycursor]


    new_result = result['data']['values']
    if len(new_result) > 10:
        new_result = new_result[:10]
    return render_template('easy_hard.html', search=new_result, enrollment=None)

@app.route("/tough", methods = ['GET', 'POST'])
def tough():
    sql = "select C.CRN, C.Subject, C.Number, C.Name, MAX(avgGPA) \
            from CoursesNew C INNER JOIN GPAsNew G on C.Subject = \
            G.CourseSubject and C.Number = G.CourseNumber WHERE \
            C.Subject = 'CS' GROUP BY C.CRN, C.Subject, C.Number, C.Name HAVING MAX(avgGPA) < 3.2;"
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record")

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    # print([type(row) for row in mycursor])
    result['data']['values'] = [row for row in mycursor]

    new_result = result['data']['values']

    
    print(new_result)
    if len(new_result) > 10:
        new_result = new_result[:10]
    return render_template('easy_hard.html', search=new_result, enrollment=None)

@app.route("/search", methods = ['GET', 'POST'])
def search():
    searchString = request.form["search-input"]

    sql = "select * from Courses;"
    
    # if sql.split()[0].upper() != "SELECT":
    #     abort(400, "must be select")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record") 

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    # print([type(row) for row in mycursor])
    result['data']['values'] = [row for row in mycursor]


    new_result = key_word_search(result['data'], searchString)
    if new_result == None:
        return render_template('easy_hard.html', search=[], enrollment=None)
    else:
        return render_template('easy_hard.html', search=new_result, enrollment=None)
        

# def check_enroll(crn, nid):
def check_pre(crn):
    sql = "select Subject, Number from Courses where CRN = " + str(crn) + " ;"
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record")    

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    result['data']['values'] = [row for row in mycursor]
    sub, num = result['data']['values'][0]
    SubNum = sub + ' ' + str(num)     

        
# def check_pre(crn):
#     sql = "select Subject, Number, Description from Courses where CRN = " + str(crn) + " ;"
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute(sql)
#     except:
#         abort(400, "fail to get record") 

#     result = {}
#     result['query_string'] = sql
#     result['data'] = {}
#     result['data']['labels'] = [row[0] for row in mycursor.description]
#     result['data']['values'] = [row for row in mycursor]
#     sub, num, des = result['data']['values'][0]
#     SubNum = sub + ' ' + str(num)
#     # pre = prerequisite(des)

#     sql = "select * from Prerequiste where CourseSubNum = '" + SubNum + "';"
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute(sql)
#     except:
#         abort(400, "fail to get record") 

#     result = {}
#     result['query_string'] = sql
#     result['data'] = {}
#     result['data']['labels'] = [row[0] for row in mycursor.description]
#     result['data']['values'] = [row for row in mycursor]

#     if (result['data']['values'] == []):
#         pre = prerequisite(des)
#         flag = update_pre(SubNum, pre)
#         if flag == True:
#             return True
#         else:
#             return check_pre(crn)
    
    




# Take CRN and NetId (HARDCODE THIS FOR NOW), insert to enrollment table, return TRUE/FALSE
@app.route("/enroll", methods = ['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        CRN = request.form['enrollBtn']
    UIN = 2000101
    sql = "select * from Enrollments where UIN = '" + str(UIN) + "' and CRN = " + str(CRN) + ";" 
    
    if sql.split()[0].upper() != "SELECT":
        abort(400, "must be select")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        pass

    if len([row for row in mycursor]) == 0:
        sql = "insert into Enrollments values (" + str(UIN) + ", " + str(CRN) + ");"
        if sql.split()[0].upper() != "INSERT":
            abort(400, "must be insert")
        
        try:
            mycursor = mydb.cursor() 
            mycursor.execute(sql)
            mydb.commit()
        except:
            abort(400, "fail to insert") 
    else:
        print('already enrolled')

    enrollment = show_enrollment()
    return render_template('easy_hard.html', search=None, enrollment=enrollment)





# Take CRN and NetId (HARDCODE THIS FOR NOW), drop row in enrollment table, return TRUE/FALSE
@app.route("/drop", methods = ['GET', 'POST'])
def drop():
    if request.method == 'POST':
        CRN = request.form['dropBtn']
    UIN = 2000101
    sql = "delete from Enrollments where UIN = '" + str(UIN) + "' and CRN = '" + str(CRN) + "';"
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
        mydb.commit()
    except:
        abort(400, "fail to get record") 

    enrollment = show_enrollment()
    return render_template('easy_hard.html', search=None, enrollment=enrollment)



# Take NetId (HARDCODE THIS FOR NOW), update row in login table, return True/FALSE
@app.route("/changePassword/", methods = ['GET', 'POST'])
def changePassword():
    originalPassword = request.form["originalpassword"]
    newPassword = request.form["newpassword"]
    NetId = 'AoWu'
    sql = "select * from Account where NetId = '" +  NetId + "' and PassWord = " + "'" + originalPassword + "';" 

    if sql.split()[0].upper() != "SELECT":
        abort(400, "must be select")
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record") 

    if len([row for row in mycursor]) == 0:
        print('wrong password, try again')
    else:
        sql = "update Account set PassWord = '" + newPassword + "' where NetID = '" + NetId + "';"

        try:
            mycursor = mydb.cursor() 
            mycursor.execute(sql)
            mydb.commit()
        except:
            abort(400, "fail to get record") 
        print('successly change password')

    enrollment = show_enrollment()
    return render_template('easy_hard.html', search=None, enrollment=enrollment)


@app.route("/enrollmentInfomation", methods = ['GET', 'POST'])
def enrollmentInfomation():
    enrollment = show_enrollment()
    return render_template('easy_hard.html', search=None, enrollment=enrollment)


# Take UIN as an parameter, return the enrollment course of this student
def show_enrollment(UIN = 2000101):

    sql = "select C.Subject, C.Number, C.Name, C.Section, C.StartTime, C.EndTime, C.DaysofWeek, C.CRN from Enrollments E join Courses C ON C.CRN = E.CRN where UIN = '" + str(UIN) + "';"
    
    try:
        mycursor = mydb.cursor() 
        mycursor.execute(sql)
    except:
        abort(400, "fail to get record") 

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    result['data']['values'] = [row for row in mycursor]

    course = result['data']['values']
    course.sort(key=lambda temp:temp[1])
    return course


if __name__ == '__main__':
    app.run('0.0.0.0', 10056, True)

