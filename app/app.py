from functools import cache
from flask_cors import CORS, cross_origin

import json
import requests
import mysql.connector

from save import *
from thread_process import *
from flask import Flask, request, jsonify

mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="admin",
    password="P@ssw0rd",
    database="smart_examination"
)
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
    return jsonify({'save-result': 'Success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
