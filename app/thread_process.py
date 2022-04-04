from util.string_util import *
from emotion_recognition import run_predict

import threading
import json

class processThread (threading.Thread):
    def __init__(self, threadName, fileName, mydb):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.fileName = fileName
        self.mydb = mydb
    def run(self):
        print ("Starting..." + self.threadName)
        process_and_save_result(self.threadName, self.fileName, self.mydb)
        print ("Exiting..." + self.threadName)

def process_and_save_result(threadName, fileName, mydb):
    exam_pin, subject_id, student_id, date = clean_text_and_get_video_data(fileName)
    total_emotion, total_emotion_time, start_end_time = run_predict(
        './app/video_storage/'+fileName)

    predictions_result = json.dumps(total_emotion)
    emotion_time = json.dumps(total_emotion_time)
    start_end = json.dumps(start_end_time)

    emotion = {
        'emotion_time': emotion_time,
        'start_end': start_end,
        'predictions_result': predictions_result
    }

    emotion_dump = json.dumps(emotion)

    update_query = "UPDATE Results SET emotion = %s WHERE student_id = %s AND exam_pin = %s"
    update_tuple = (
        emotion_dump,
        student_id, 
        exam_pin,   
        )
    cursor = mydb.cursor()
    try:
        result = cursor.execute(update_query, update_tuple)
        mydb.commit()
        print("thread -> Success result")
        return result
    except Exception as e:
        print("thread -> Error result: ", e)
        return e

    threadName.exit()
