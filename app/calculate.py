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
    exam_items_time_stamp = data['exam_items_time_stamp']
    emotion = data['emotion']

    emotion_time_per_user = []
    for item in emotion:
        for user_result in item:
            emotion_time = user_result.get('emotion_time')
            if emotion_time is not None:
                emotion_time_per_user.append(emotion_time)
    
    emotion_per_item = {}
    for user_user, user_time_per_item in enumerate(exam_items_time_stamp):
        for item_index, time_stamp in enumerate(user_time_per_item):
            item_emote = {'angry': 0, 'happy': 0, 'neutral': 0, 'sad': 0}
            for item in time_stamp:
                angry_count = 0
                happy_count = 0
                neutral_count = 0
                sad_count = 0

                for emote in emotion_time_per_user:
                    angry = emote.get('angry')
                    happy = emote.get('happy')
                    neutral = emote.get('neutral')
                    sad = emote.get('sad')

                    for angry_item in angry:
                        if item[0] <= angry_item and item[1] >= angry_item:
                            angry_count += 1
                    for happy_item in happy:
                        if item[0] <= happy_item and item[1] >= happy_item:
                            happy_count += 1
                    for neutral_item in neutral:
                        if item[0] <= neutral_item and item[1] >= neutral_item:
                            neutral_count += 1
                    for sad_item in sad:
                        if item[0] <= sad_item and item[1] >= sad_item:
                            sad_count += 1

                item_emote['angry'] += angry_count
                item_emote['happy'] += happy_count
                item_emote['neutral'] += neutral_count
                item_emote['sad'] += sad_count

            is_init_emotion_per_item = emotion_per_item.get(item_index)

            if is_init_emotion_per_item:
                emotion_per_item[item_index]['angry'] += item_emote['angry']
                emotion_per_item[item_index]['happy'] += item_emote['happy']
                emotion_per_item[item_index]['neutral'] += item_emote['neutral']
                emotion_per_item[item_index]['sad'] += item_emote['sad']
            else:
                emotion_per_item[item_index] = item_emote

    percent_of_emote_per_item = {}
    for emote_index, emote in emotion_per_item.items():
        percent_of_emote_per_item[emote_index+1] = get_emote_percent(emote)

    return {'percent_of_emote':percent_of_emote_per_item}

def get_emote_percent(all_emote):
    sum_emote = sum(all_emote.values())

    angry = all_emote['angry']
    happy = all_emote['happy']
    neutral = all_emote['neutral']
    sad = all_emote['sad']

    percent_of_angry = calculate_percent(angry, sum_emote)
    percent_of_happy = calculate_percent(happy, sum_emote)
    percent_of_neutral = calculate_percent(neutral, sum_emote)
    percent_of_sad = calculate_percent(sad, sum_emote)

    percent_emote = {'angry': percent_of_angry, 'happy': percent_of_happy, 'neutral': percent_of_neutral, 'sad': percent_of_sad}
    return percent_emote

def calculate_percent(x, y):
    try:
        return round((x / y * 100), 2)
    except Exception as e:
        return 0

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