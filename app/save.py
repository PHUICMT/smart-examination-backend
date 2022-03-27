from util.string_util import *

import os
from datetime import datetime
import mysql.connector
import uuid

UPLOAD_FOLDER = './app/video_storage'
mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="admin",
    password="P@ssw0rd",
    database="smart_examination"
)
cursor = mydb.cursor()

now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S')


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
    answer = request.json['resultPerItems']
    start_and_end_time = request.json['startAndEndTime']
    exam_items_time_stamp = request.json['examItemsTimeStamp']
   
    sql_insert_query = " INSERT INTO Results (id, student_id, exam_pin, answer, start_and_end_time, exam_items_time_stamp) VALUES (%s,%s,%s,%s,%s,%s)"
    insert_tuple = (
        result_id,
        studentId,
        exam_pin,
        answer,
        start_and_end_time,
        exam_items_time_stamp)
    return execute_database(sql_insert_query, insert_tuple)

def execute_database(sql_insert_query, insert_tuple):
    try:
        result = cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
        return result
    except Exception as e:
        return e
    