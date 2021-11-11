from flask import Flask, render_template, request, abort
import mysql.connector
import re
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
app = Flask(__name__) 

mydb = mysql.connector.connect(
            host='localhost',
            user='yiyanw3',
            database='yiyanw3_database',
            password='!1234QWERasdf')

@app.route('/', methods=['GET'])
def loginPage():
    return render_template('enroll.html', search=None, enrollment=None)

# # http://20.88.14.242:10056/delete query_string drop table Test
# @app.route("/delete", methods = ['POST'])
# def deleteSth():
#     sql = request.form['query_string']
#     if sql.split()[0].upper() != "DELETE" and sql.split()[0].upper() != "DROP":
#         abort(400, "must be create")
    
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute(sql)
#         mydb.commit()
#     except:
#         abort(400, "fail to create table") 

#     return 'success'

# # postman: http://20.88.14.242:10056/create  key:query_string value:create table acc ( number   char(3))
# @app.route("/create", methods = ['POST'])
# def newTable():
#     sql = request.form['query_string']
#     if sql.split()[0].upper() != "CREATE":
#         abort(400, "must be create")
    
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute(sql)
#         mydb.commit()
#     except:
#         abort(400, "fail to create table") 

#     return 'success'

# # http://20.88.14.242:10056/insert key:query_string value:insert into account values (101, 'J. Smith', 1000.00, 'checking')
# @app.route("/insert", methods = ['POST'])
# def insertRecord():
#     sql = request.form['query_string']
#     print(sql)
#     if sql.split()[0].upper() != "INSERT":
#         abort(400, "must be insert")
    
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute("SET FOREIGN_KEY_CHECKS=0;")
#         mycursor.execute(sql)
#         mydb.commit()
#     except:
#         abort(400, "fail to insert record") 

#     return 'success'


# @app.route("/update", methods = ['POST'])
# def updateRecord():
#     sql = request.form['query_string']
#     print(sql)
    
#     try:
#         mycursor = mydb.cursor()
#         mycursor.execute(sql)
#         mydb.commit()
#     except:
#         abort(400, "fail to update") 

#     return 'success'

# # http://20.88.14.242:10056/select key:query_string values:select * from account
# @app.route("/select", methods = ['GET'])
# def showRecord():
#     sql = request.form['query_string']
    
#     if sql.split()[0].upper() != "SELECT":
#         abort(400, "must be select")
    
#     try:
#         mycursor = mydb.cursor() 
#         mycursor.execute(sql)
#     except:
#         abort(400, "fail to get record") 

#     # print([type(row[0]) for row in mycursor.description]) 
#     # print([row for row in mycursor])
#     result = {}
#     result['query_string'] = sql
#     result['data'] = {}
#     result['data']['labels'] = [row[0] for row in mycursor.description]
#     # print([type(row) for row in mycursor])
#     result['data']['values'] = [row for row in mycursor]
#     result['data']['values']
#     return result


def key_word_search(result, key_word):
    '''
    input:
    df: pandas dataframe, contain all courses infomation
    key_word: string

    return: 
    df_out: pandas dataframe, contain all courses info relate to key word
    '''

    labels = result['labels']
    values = result['values']
    new_values = None
    df = pd.DataFrame(values, columns=labels)
    if key_word.isalpha():
        # subject search
        if len(key_word) >=2 and len(key_word) <= 4:
            sub = key_word.upper()
            df_sub = df[df['Subject'] == sub]
            if len(df_sub) > 0:
                df_out = df_sub
                records = df_out.to_records(index=False)
                new_values = list(records)
                if len(new_values) > 10:
                    new_values = new_values[:10]
                new_values.sort(key=lambda course: course[5])
                return new_values
                
    else:
        ints = re.findall("\d", key_word)
        alphas = re.findall('[A-Za-z]', key_word)
        if len(ints) == 3 and len(alphas) > 0:
            num = int(ints[0] + ints[1] + ints[2])
            df_num = df[df['Number'] == num]
            if len(df_num) == 0:
                pass
            else: 
                if len(alphas) <=4 and len(alphas) >= 2:
                    sub = ''.join(alphas)
                    sub = sub.upper()
                    df_sub_num = df_num[df_num['Subject'] == sub]
                    if len(df_sub_num) == 0:
                        pass
                    else:
                        df_out = df_sub_num
                        records = df_out.to_records(index=False)
                        new_values = list(records)
                        if len(new_values) > 10:
                            new_values = new_values[:10]
                        new_values.sort(key=lambda course: course[5])
                        return new_values


        elif len(ints) == 1 and len(alphas) > 0:
            num = int(ints[0])
            df_num = df[df['Number'] // 100 == num]
            if len(df_num) == 0:
                pass
            else: 
                if len(alphas) <=4 and len(alphas) >= 2:
                    sub = ''.join(alphas)
                    sub = sub.upper()
                    df_sub_num = df_num[df_num['Subject'] == sub]
                    if len(df_sub_num) == 0:
                        pass
                    else:
                        df_out = df_sub_num
                        records = df_out.to_records(index=False)
                        new_values = list(records)
                        if len(new_values) > 10:
                            new_values = new_values[:10]
                        new_values.sort(key=lambda course: course[5])
                        return new_values
        
        elif len(ints) == 3 and len(alphas) == 0:
            num = int(ints[0] + ints[1] + ints[2])
            df_num = df[df['Number'] == num]
            if len(df_num) == 0:
                pass
            else:
                df_out = df_num
                records = df_out.to_records(index=False)
                new_values = list(records)
                if len(new_values) > 10:
                    new_values = new_values[:10]
                new_values.sort(key=lambda course: course[5])
                return new_values
        else:
            pass

    df_apply = df.apply(
        lambda row: fuzz.partial_ratio(row['Name'], key_word), axis=1
    )
    df_out = df[df_apply > 70]
    records = df_out.to_records(index=False)
    new_values = list(records)
    
    if len(new_values) > 10:
        new_values = new_values[:10]

    return new_values


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

    # print([type(row[0]) for row in mycursor.description]) 
    # print([row for row in mycursor])
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
        # crn = []
        # subject = []
        # number = []
        # for i in range(len(new_result)):
        #     # print(new_result[i][4], new_result[i][5], new_result[i])
        #     crn.append(new_result[i][0])
        #     subject.append("'" + new_result[i][4] + "'")
        #     number.append(str(new_result[i][5]))
        
        # # subject_name = subject.copy()
        # # for i in range(len(number)):
        # #     subject_name[i] = "'" + subject[i] + str(number[i]) + "'"
        # # sn = ', '.join(subject_name)

        # s = ', '.join(subject)
        # n = ', '.join(number)


        # sql =  "select C.Subject, C.Number, SUM(avgGPA * countGPA) / SUM(countGPA) as average_GPA \
        #         from GPAs G join CoursesNew C on G.NetId = C.NetId and G.CourseSubject = C.Subject and G.CourseNumber = C.Number \
        #         where C.subject in (" + s + ") group by C.Subject, C.Number \
        #         intersect \
        #         select C.Subject, C.Number, SUM(avgGPA * countGPA) / SUM(countGPA) as average_GPA \
        #         from GPAs G join CoursesNew C on G.NetId = C.NetId and G.CourseSubject = C.Subject and G.CourseNumber = C.Number \
        #         where C.Number in (" + n + ") group by C.Subject, C.Number ;"
        # print(sql)        
        
        # mycursor = mydb.cursor() 
        # mycursor.execute(sql)

        # # agpa = {}
        # # agpa['query_string'] = sql
        # # agpa['data'] = {}
        # # agpa['data']['labels'] = [row[0] for row in mycursor.description]
        # agpa = [row for row in mycursor]
        # new_result += agpa 


        return render_template('enroll.html', search=new_result, enrollment=None)
        

# def check_enroll(crn, nid):

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
    return render_template('enroll.html', search=None, enrollment=enrollment)


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

