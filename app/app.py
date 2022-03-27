from functools import cache
from flask_cors import CORS, cross_origin

import json
import requests
import pika

from save import *
from thread_process import *
from emotion_recognition import run_predict
from flask import Flask, request, jsonify

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'

# credentials = pika.PlainCredentials('admin', 'admin')
# parameters = pika.ConnectionParameters(
#     host='rabbitmq', port='5672', heartbeat=0, credentials=credentials)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()


global predictions_result

@app.route('/upload-video', methods=['POST'])
def upload_webcam_file():

    uploaded_file = request.files['file']
    fileName = request.form.get("fileName", False)
    save_video_result = save_video(uploaded_file, fileName)

    start_process = processThread('Thread-'+fileName, fileName)
    start_process.start()
    start_process.join()

    return jsonify({'upload-result':'Success'}), 200

@app.route('/save-result', methods=['POST'])
def save_result():
    result = save_result_to_database(request)
    return jsonify({'save-result': 'Success'}), 200

# @app.route('/process-video', methods=['POST'])
# def process_webcam():
    # all_json = request.get_json()
    # uuid = request.json['uuid']
    # filename = "["+uuid+"]"+'webcam.webm'
    # total_emotion, total_emotion_time, start_end_time = run_predict(
    #     './app/video_storage/'+filename)
    # predictions_result = json.dumps(total_emotion)
    # save_backend_result_to_database(uuid, predictions_result)
    # channel.queue_declare(queue='dataFromBackend', durable=True)
    # message = json.dumps({
    #     "predictions_result": predictions_result,
    #     "total_emotion_time": total_emotion_time,
    #     "start_end_time": start_end_time,
    #     "all_json": all_json
    # })
    # channel.basic_publish(
    #     exchange='',
    #     routing_key='dataFromBackend',
    #     body=message
    # )
#     return jsonify({"response": "RabbitMQ Accepted!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
