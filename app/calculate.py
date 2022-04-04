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
    data = combine_result_data(result)
    emotion = data['emotion']

    for item in emotion:
        for user_result in item:
            for key, value in user_result.items():
                print(key)
        print('\n')
                
    
    return {
        'average_score': data['average_score'],
        'exam_items_time_stamp': data['exam_items_time_stamp']
    }

def get_execute_database(sql_insert_query):
    if mydb is None:
        return False
    cursor = mydb.cursor()
    try:
        cursor.execute(sql_insert_query)
        result = cursor.fetchall()
        print("calculate.py -> Success result")
        return result
    except Exception as e:
        print("calculate.py -> Error result: " + str(e))
        return e
    mydb.close()

def combine_result_data(result):
    all_score = [data[0] for data in result]
    all_time_stamp = [json.loads(data[2]) for data in result]

    all_emote = [json.loads(data[1]) for data in result]
    all_emote_list = [data for data in all_emote]

    all_emote_json = []
    for data in all_emote_list:
        user_result = [{key: json.loads(value)} for key, value in data.items()]
        all_emote_json.append(user_result)

    average_score = calculate_average(all_score)
    return {
            'average_score': average_score,
            'emotion': all_emote_json,
            'exam_items_time_stamp': all_time_stamp
        }

def calculate_average(data):
    total_score = 0
    try:
        for item in data:
            total_score += item
        return total_score / len(data)
    except Exception as e:
        return 0