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
    video_uuid = str(uuid.uuid4())
    print("UUID : " + video_uuid)

    exam_pin, subject_id, student_id, date = clean_text_and_get_video_data(filename)
    print(exam_pin)
    print(student_id)
    print(subject_id)
    print(date)

    filePath = os.path.join(UPLOAD_FOLDER, filename)
    created_file = open(filePath,"w+")
    file.save(filePath)
    sql_insert_blob_query = " INSERT INTO Videos (id, file_name, student_id, subject_id, exam_pin, created_at) VALUES (%s,%s,%s,%s,%s,%s)"
    insert_blob_tuple = (
        video_uuid, 
        filename, 
        student_id, 
        subject_id, 
        exam_pin, 
        date.replace('_',"/")
        )
    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    mydb.commit()
    return 'Saved!'

def clean_text_and_get_video_data(text):
    char_to_replace = {'[',']','.webm'}
    replaced_text = text
    for key in char_to_replace:
        replaced_text = replaced_text.replace(key, '')
    return replaced_text.split('-')

# def save_result_to_database(student_id, exam_pin):
#     sql_insert_query = " UPDATE Result SET emotion=%s WHERE questionnaire_id=%s"
#     insert_tuple = (emotion, questionnaire_id)
#     result = cursor.execute(sql_insert_query, insert_tuple)
#     mydb.commit()
#     return result
