from util.string_util import *

import os
from datetime import datetime
import json

UPLOAD_FOLDER = './app/video_storage'

now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S')
mydb = None

def save_video(file, filename):
    video_uuid = genarate_uuid()
    exam_pin, subject_id, student_id, date = clean_text_and_get_video_data(filename)

    filePath = os.path.join(UPLOAD_FOLDER, filename)
    created_file = open(filePath,"w+")
    file.save(filePath)
    created_file.close()

    sql_insert_query = " INSERT INTO Videos (id, file_name, student_id, subject_id, exam_pin, created_at) VALUES (%s,%s,%s,%s,%s,%s)"
    insert_tuple = (
        video_uuid, 
        filename, 
        student_id, 
        subject_id, 
        exam_pin,   
        date.replace('_',"/")
        )

    return execute_database(sql_insert_query, insert_tuple)


def save_result_to_database(request):
    result_id = genarate_uuid()
    studentId = request.json['studentId']
    exam_pin = request.json['examPin']
    answer = json.dumps(request.json['resultPerItems'])
    start_and_end_time = json.dumps(request.json['startAndEndTime'])
    exam_items_time_stamp = json.dumps(request.json['examItemsTimeStamp'])
   
    sql_insert_query = " INSERT INTO Results (id, student_id, exam_pin, answer, start_and_end_time, exam_items_time_stamp) VALUES (%s,%s,%s,%s,%s,%s)"
    insert_tuple = (
        result_id,
        studentId,
        exam_pin,
        answer,
        start_and_end_time,
        exam_items_time_stamp)
    return execute_database(sql_insert_query, insert_tuple)

def save_exam_to_database(request):
    exam_pin = request.json['examPin']
    exam_name = request.json['examName']
    teacher_id = request.json['teacherId']
    items_count = request.json['itemCount']
    score = request.json['score']
    exam = json.dumps(request.json['examItems'])
   
    sql_insert_query = " INSERT INTO Examination (exam_pin, exam_name, teacher_id, items_count, score, exam, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    insert_tuple = (
        exam_pin,
        exam_name,
        teacher_id,
        items_count,
        score,
        exam,
        current_time
    )
    return execute_database(sql_insert_query, insert_tuple)

def check_user_id_exist(request):
    user_id = request.json['userId']
    sql_query = "SELECT user_id FROM Users WHERE user_id='" + user_id + "'"
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
        print("save.py -> Success result: Saved!")
        return result
    except Exception as e:
        print("save.py -> Error result: ", e)
        return e
    