from functools import cache
import json
import requests
import pika

from save import save_video, save_questionnaire_to_database, save_backend_result_to_database, save_fontend_result_to_database, questionnaire_count
from emotion_recognition import run_predict
from flask import Flask, request, jsonify

app = Flask(__name__)
credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters(
    host='rabbitmq', port='5672', heartbeat=0, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


global predictions_result

@app.route('/upload-video', methods=['POST'])
def upload_webcam_file():
    uploaded_file = request.files['blob']
    uuid = request.form.get("uuid", False)
    filename = "["+uuid+"]"+'webcam.webm'
    save_video_result = save_video(uploaded_file, uuid, True, filename)
    return jsonify({"save_video": save_video_result})


@app.route('/process-video', methods=['POST'])
def process_webcam():
    all_json = request.get_json()
    uuid = request.json['uuid']
    filename = "["+uuid+"]"+'webcam.webm'
    total_emotion, total_emotion_time, start_end_time = run_predict(
        './app/video_storage/'+filename)
    predictions_result = json.dumps(total_emotion)
    save_backend_result_to_database(uuid, predictions_result)
    channel.queue_declare(queue='dataFromBackend', durable=True)
    message = json.dumps({
        "predictions_result": predictions_result,
        "total_emotion_time": total_emotion_time,
        "start_end_time": start_end_time,
        "all_json": all_json
    })
    channel.basic_publish(
        exchange='',
        routing_key='dataFromBackend',
        body=message
    )

    return jsonify({"response": "RabbitMQ Accepted!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
