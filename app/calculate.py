import json

mydb = None

def set_db(mydb_input):
    global mydb
    mydb = mydb_input

def get_exam_result_from_database(examPin):
    get_result_query = "SELECT total_score, emotion, exam_items_time_stamp FROM Results WHERE exam_pin='" + examPin + "'"
    result = get_execute_database(get_result_query)
    if result is None:
        return None
    all_score = [data[0] for data in result]
    all_emote = [json.loads(data[1]) for data in result]
    all_time_stamp = [json.loads(data[2]) for data in result]

    average_score = calculate_average(all_score)
    data = {
            'total_score': all_score,
            'emotion': all_emote,
            'exam_items_time_stamp': all_time_stamp
        }
    return data

def get_execute_database(sql_insert_query):
    if mydb is None:
        return False
    cursor = mydb.cursor()
    try:
        cursor.execute(sql_insert_query)
        result = cursor.fetchall()
        print("calculate.py -> Success result: Saved!")
        return result
    except Exception as e:
        print("calculate.py -> Error result: ", e)
        return e
    mydb.close()

def calculate_average(data):
    total_score = 0
    for item in data:
        total_score += item
    return total_score / len(data)