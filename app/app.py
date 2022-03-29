from functools import cache
from flask_cors import CORS, cross_origin

import json
import requests
import mysql.connector

from save import *
from get import *
from thread_process import *
from flask import Flask, request, jsonify

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="admin",
    password="P@ssw0rd",
    database="smart_examination",
    use_unicode=True, 
    charset='utf8'
)
mydb.set_charset_collation(charset='utf8', collation='utf8_general_ci')

set_db(mydb)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'


global predictions_result

@app.route('/upload-video', methods=['POST'])
def upload_webcam_file():

    uploaded_file = request.files['file']
    fileName = request.form.get("fileName", False)
    save_video_result = save_video(uploaded_file, fileName)

    start_process = processThread('Thread-'+fileName, fileName, mydb)
    start_process.start()
    start_process.join()

    return jsonify({'upload-result':'Success'}), 200

@app.route('/save-result', methods=['POST'])
def save_result():
    result = save_result_to_database(request)
    return jsonify({'save-result': True}), 200

@app.route('/save-exam', methods=['POST'])
def save_exam():
    result = save_exam_to_database(request)
    return jsonify({'save-exam': True}), 200

@app.route('/get-exam', methods=['GET'])
def get_exam():
    examPin = request.args.get('exampin')
    try:
        exam = get_exam_from_database(examPin)
        data = json.loads(exam[0][0])
        return jsonify({'exam_items': data}), 200
    except:
        return jsonify({'exam_items': False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
