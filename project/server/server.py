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
            user='root',
            database='',
            password='')


@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route('/', methods=['GET'])
def mainPage():
    return render_template('enroll.html', search=None, enrollment=None)



@app.route("/rec", methods = ['GET', 'POST'])
def rec():
    mycursor = mydb.cursor()
    args = [2000101, 'CS']
    mycursor.callproc('findRecommendation', args)
    result = []
    for i in mycursor.stored_results():
        new_result = i.fetchall()


    # result['query_string'] = ""
    # result['data'] = {}
    # result['data']['labels'] = [row[0] for row in mycursor.description]
    # # print([type(row) for row in mycursor])
    # result['data']['values'] = [row for row in mycursor]

    # new_result = result['data']['values']



    # if len(new_result) > 10:
    #     new_result = new_result[:10]
    return render_template('rec.html', search=list(set(new_result)), enrollment=None)

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
        return render_template('enroll.html', search=[], enrollment=None)
    else:
        return render_template('enroll.html', search=new_result, enrollment=None)

# join Courses on Enrollments.CRN = Courses.CRN \
# def check_enroll(crn, nid):
def check_pre(UIN, SubNum):

    sql = "select L.CSN from \
        (select CSN, SEPSN from\
        (select CSN, PSN, Sum(CEPSN >= 1) as SEPSN from\
        (select CSN, PSN, Count(EPSN) as CEPSN from \
        (select distinct Prerequisite.CourseSubNum as CSN, \
        Prerequisite.PreSubNum as PSN, Prerequisite.EquPreSubNum as EPSN \
        from Students join Enrollments on Students.UIN = Enrollments.UIN \
        join (select concat(Subject, ' ', Number) as SubNum, CRN from Courses) T on T.CRN = Enrollments.CRN \
        join Prerequisite on T.SubNum = Prerequisite.EquPreSubNum where Students.UIN = " + str(UIN) + ") M \
        GROUP BY CSN, PSN) N\
        GROUP BY CSN, PSN) K) P\
        join\
        (select CourseSubNum as CSN, Count(PreSubNum)  as CPSN\
        from (select distinct CourseSubNum, PreSubNum from Prerequisite) A join\
        (select distinct Prerequisite.CourseSubNum as CSN \
        from Students join Enrollments on Students.UIN = Enrollments.UIN\
        join (select concat(Subject, ' ', Number) as SubNum, CRN from Courses) T on T.CRN = Enrollments.CRN \
        join Prerequisite on T.SubNum = Prerequisite.EquPreSubNum where Students.UIN = " + str(UIN) + ") M \
        on M.CSN = A.CourseSubNum\
        GROUP BY CourseSubNum) L\
        on P.CSN = L.CSN\
        Where P.SEPSN = L.CPSN;"

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

    for i in result['data']['values']:
        if i[0] == SubNum:
            return True
    return False











# Take CRN and NetId (HARDCODE THIS FOR NOW), insert to enrollment table, return TRUE/FALSE
@app.route("/enroll", methods = ['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        CRN = request.form['enrollBtn']
    UIN = 2000101
    sql = "select Subject, Number from Courses where CRN = " + str(CRN) + ";"
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except:
        pass

    result = {}
    result['query_string'] = sql
    result['data'] = {}
    result['data']['labels'] = [row[0] for row in mycursor.description]
    result['data']['values'] = [row for row in mycursor]

    sub, num = result['data']['values'][0]
    subNum = sub + " " + str(num)
    print(subNum)
    if check_pre(UIN, subNum) == False:
        print("Unable to enroll")
        return render_template('enroll.html', search=None, enrollment=None)
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
    return render_template('enroll.html', search=None, enrollment=enrollment)





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
    return render_template('enroll.html', search=None, enrollment=enrollment)



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
    return render_template('enroll.html', search=None, enrollment=enrollment)


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
