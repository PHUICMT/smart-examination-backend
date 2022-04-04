def check_user_id_exist(request):
    user_id = request.json['userId']
    sql_query = "SELECT user_id FROM Users WHERE user_id='" + user_id + "'"
    result = execute_database(sql_query, None)
    if len(result) <= 0:
        return False
    return True

def check_result_exist(request):
    student_id = request.json['studentId']
    exam_pin = request.json['examPin']
    sql_query = "SELECT student_id FROM Results WHERE student_id='" + student_id + "' AND exam_pin='" + exam_pin + "'"
    result = execute_database(sql_query, None)
    if len(result) <= 0:
        return False
    return True

def set_db(mydb_input):
    global mydb
    mydb = mydb_input

def execute_database(sql_insert_query, insert_tuple):
    if mydb is None:
        return False

    cursor = mydb.cursor()
    result = None
    try:
        if insert_tuple is None:
            cursor.execute(sql_insert_query)
        else:
            cursor.execute(sql_insert_query, insert_tuple)
            
        result = cursor.fetchall()
        mydb.commit()
        print("verify.py -> Success result")
        return result
    except Exception as e:
        print("verify.py -> Error result: ", e)
        return e