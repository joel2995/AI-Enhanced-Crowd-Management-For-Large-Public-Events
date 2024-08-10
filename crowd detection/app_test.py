from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import threading
import time


app = Flask(__name__)

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
ALERT_THRESHOLD = 3

net = cv2.dnn.readNet("C:/Users/DEEPAN/Desktop/Hackmageddon/FIVEDEVELOPERS/crowd detection/yolov3.weights", "C:/Users/DEEPAN/Desktop/Hackmageddon/FIVEDEVELOPERS/crowd detection/yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

names_path = "C:/Users/DEEPAN/Desktop/Hackmageddon/FIVEDEVELOPERS/crowd detection/coco.names"

with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


people_count = 0
people_count_history = []
lock = threading.Lock()

def detect_people():
    global people_count, people_count_history
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (1000, 1000))
        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > CONFIDENCE_THRESHOLD and class_id == 0:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

        people_count = 0
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                center_x = x + w // 2
                center_y = y + h // 2
                radius = int((w + h) / 4)
                label = str(classes[class_ids[i]])
                if label == 'person':
                    people_count += 1
                    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
                    cv2.putText(frame, label, (center_x - radius, center_y - radius - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No person detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f'People Count: {people_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        with lock:
            people_count_history.append(people_count)
            if len(people_count_history) > 100:
                people_count_history.pop(0)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_people(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/chart_data')
def chart_data():
    with lock:
        data = {
            'count': people_count_history
        }
    return jsonify(data)

@app.route('/alert')
def alert():
    with lock:
        alert = people_count >= ALERT_THRESHOLD
    return jsonify({'alert': alert})

if __name__ == '__main__':
    app.run(debug=True)
