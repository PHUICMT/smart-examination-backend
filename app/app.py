# from functools import cache
from flask_cors import CORS, cross_origin

import json
import requests
import mysql.connector

import save as save
import get as get
import calculate as cal
import verify as verify

from thread_process import *
from flask import Flask, request, jsonify

mydb = mysql.connector.connect(
    host="db",
    port="3306",
    user="admin",
    password="P@ssw0rd",
    database="smart_examination",
    use_unicode=True,
    charset='utf8'
)
mydb.set_charset_collation(charset='utf8', collation='utf8_general_ci')

save.set_db(mydb)
get.set_db(mydb)
cal.set_db(mydb)
verify.set_db(mydb)

app = Flask(__name__)
cors = CORS(app, allow_headers=['Content-Type', 'Access-Control-Allow-Origin',
                                'Access-Control-Allow-Headers', 'Access-Control-Allow-Methods'])

app.config['CORS_HEADERS'] = '*'


global predictions_result


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, " + \
        "X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response


@app.route('/upload-video', methods=['POST'])
def upload_webcam_file():

    uploaded_file = request.files['file']
    fileName = request.form.get("fileName", False)
    save_video_result = save.save_video(uploaded_file, fileName)

    start_process = processThread('Thread-'+fileName, fileName, mydb)
    start_process.start()
    start_process.join()

    return jsonify({'upload-result': 'Success'}), 200


@app.route('/save-result', methods=['POST'])
def save_result():
    result = save.save_result_to_database(request)
    return jsonify({'save-result': True}), 200


@app.route('/save-exam', methods=['POST'])
def save_exam():
    result = save.save_exam_to_database(request)
    return jsonify({'save-exam': True}), 200


@app.route('/login', methods=['POST'])
def login():
    result = verify.check_user_id_exist(request)
    return jsonify({'login': result}), 200


@app.route('/get-exam', methods=['GET'])
def get_exam():
    examPin = request.args.get('exampin')
    try:
        exam = get.get_exam_from_database(examPin)
        data = {
            'exam_pin': exam[0][0],
            'exam_subject': exam[0][1],
            'exam_title': exam[0][2],
            'exam_description': exam[0][3],
            'teacher_id': exam[0][4],
            'exam': json.loads(exam[0][5]),
            'created_at': exam[0][6]
        }
        return jsonify({'exam_items': data}), 200
    except Exception as e:
        return jsonify({'exam_items': False}), 200


@app.route('/get-exam-all', methods=['GET'])
def get_exam_all():
    try:
        exam = get.get_exam_all_from_database()
        data = []
        for i in range(0, len(exam)):
            data.append({
                'exam_pin': exam[i][0],
                'exam_subject': exam[i][1],
                'exam_title': exam[i][2],
                'exam_description': exam[i][3],
                'teacher_id': exam[i][4],
                'exam': json.loads(exam[i][5]),
                'created_at': exam[i][6]
            })

        return jsonify({'exam_items': data}), 200
    except Exception as e:
        return jsonify({'exam_items': False}), 200


@app.route('/get-result', methods=['GET'])
def get_result():
    examPin = request.args.get('exampin')
    try:
        data = cal.get_exam_result_from_database(examPin)
        return jsonify({'result': data}), 200
    except Exception as e:
        return jsonify({'result': False}), 200


@app.route('/get-subject', methods=['GET'])
def get_subject():
    try:
        subject = get.get_subject_from_database()
        data = []
        for i in range(0, len(subject)):
            data.append({
                'subject_id': subject[i][0],
                'name': subject[i][1],
            })

        return jsonify({'subject_items': data}), 200
    except Exception as e:
        return jsonify({'subject_items': False}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
