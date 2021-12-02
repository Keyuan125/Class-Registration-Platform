

def update_pre(CourseSubNum, pre_list):
    '''
    prerequisite table:
    Prerequiste: CourseSubNum, PreSubNum, EquPreSubNum
    '''
    if pre_list == []:
        return True
    typelist = type([1])
    
    for i in range(len(pre_list)):
        if type(pre_list[i]) == typelist:
            update_pre(CourseSubNum, pre_list[i])
        else:
            PreSubNum = pre_list[0]
            EquPreSubNum = pre_list[i]
            if len(EquPreSubNum) > 10 or len(PreSubNum) > 10:
                continue
            print(PreSubNum, EquPreSubNum)
            sql = "insert into Prerequisite values (0, '" + CourseSubNum + "', '" + PreSubNum + "', '" + EquPreSubNum + "');"
            print(sql)
            try:
                mycursor = mydb.cursor() 
                mycursor.execute(sql)
                mydb.commit()
            except:
                abort(400, "fail to insert") 
    return False

def insert_pre():
    sql = "select Subject, Number, Description from Courses group by Subject, Number, Description"
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

    for sub, num, des in result['data']['values']:
        SubNum = sub + ' ' + str(num)
        pre = prerequisite(des)
        update_pre(SubNum, pre)
