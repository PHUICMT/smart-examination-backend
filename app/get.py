mydb = None


def set_db(mydb_input):
    global mydb
    mydb = mydb_input


def get_exam_from_database(examPin):
    sql_query = "SELECT * FROM Examination WHERE exam_pin='" + examPin + "'"
    return get_execute_database(sql_query)


def get_exam_all_from_database():
    sql_query = "SELECT * FROM Examination"
    return get_execute_database(sql_query)


def get_subject_from_database():
    sql_query = "SELECT * FROM Subject"
    return get_execute_database(sql_query)


def get_execute_database(sql_insert_query):
    if mydb is None:
        return False
    cursor = mydb.cursor()
    try:
        cursor.execute(sql_insert_query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        return e
    mydb.close()
