import os
from datetime import datetime
import mysql.connector

UPLOAD_FOLDER = './app/video_storage'
# mydb = mysql.connector.connect(
#     host="db",
#     user="admin",
#     password="P@ssw0rd",
#     database="phq_9_db"
# )
# cursor = mydb.cursor()

now = datetime.now()
current_time = now.strftime('%Y-%m-%d %H:%M:%S')


def save_video(file, questionnaire_id, video_type, filename):
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    # sql_insert_blob_query = " INSERT INTO Videos (video_name, questionnaire_id, video_type_is_webcam) VALUES (%s,%s,%s)"
    # insert_blob_tuple = (filename, questionnaire_id, video_type)
    # result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
    # mydb.commit()
    return 'Saved! and Save to Database'


# def save_backend_result_to_database(questionnaire_id, emotion):
#     sql_insert_query = " UPDATE Result SET emotion=%s WHERE questionnaire_id=%s"
#     insert_tuple = (emotion, questionnaire_id)
#     result = cursor.execute(sql_insert_query, insert_tuple)
#     mydb.commit()
#     return result
