import cv2
import numpy as np
import imutils
from collections import deque
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
import time

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
GRAPH_LENGTH = 50 
ALERT_THRESHOLD = 10

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

video_path = r'C:\Users\user\OneDrive\Desktop\Hackathon Projects\CCTV Analysis\4196258-hd_1280_720_30fps.mp4'
cap = cv2.VideoCapture(video_path)

people_count_history = deque(maxlen=GRAPH_LENGTH)

def alert_popup():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Alert", "People count has exceeded the threshold! Consider reducing the number of people or improving space utilization.")

def show_alert_popup():
    threading.Thread(target=alert_popup, daemon=True).start()

fig, ax = plt.subplots()
ax.set_xlim(0, GRAPH_LENGTH)
ax.set_ylim(0, 50) 
line, = ax.plot([], [], 'b-')
ax.set_xlabel('Frame')
ax.set_ylabel('People Count')
ax.set_title('People Count Over Time')

def update_graph(frame):
    line.set_xdata(range(len(people_count_history)))
    line.set_ydata(people_count_history)
    ax.relim()
    ax.autoscale_view()
    return line,

def graph_thread():
    ani = FuncAnimation(fig, update_graph, interval=1000, blit=True)
    plt.show()

threading.Thread(target=graph_thread, daemon=True).start()

def process_video():
    last_alert_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = imutils.resize(frame, width=600)
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
                label = str(classes[class_ids[i]])
                if label == 'person':
                    people_count += 1
                    color = (0, 0, 255) if people_count > ALERT_THRESHOLD else (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        else:
            cv2.putText(frame, 'No person detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        people_count_history.append(people_count)
        cv2.putText(frame, f'People Count: {people_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Webcam", frame)
        current_time = time.time()
        if people_count > ALERT_THRESHOLD and (current_time - last_alert_time) > 20:  # Avoid showing multiple alerts in quick succession
            show_alert_popup()
            last_alert_time = current_time
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
threading.Thread(target=process_video, daemon=True).start()

plt.show(block=True) 
cap.release()
cv2.destroyAllWindows()
