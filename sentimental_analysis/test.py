import os
from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace
import numpy as np
import mediapipe as mp
from collections import Counter
import time
from scipy.spatial import distance as dist

app = Flask(__name__, template_folder='C:/Users/user/OneDrive/Desktop/Hackathon Projects/CCTV Analysis/templates')

# Initialize global variables
cap = cv2.VideoCapture(1)  # Change the index if needed (0 for built-in, 1 for external, etc.)
start_time = time.time()
sentiments_over_time = []
behaviors_over_time = []
anomaly_times = []
anomaly_count = 0
previous_position = None
anomaly_detected = False
sentiment_counter = Counter({"Great event!": 0, "Too crowded": 0, "Felt unsafe": 0, "Amazing experience": 0})
behavior_counter = Counter({"Hand movement detected": 0, "No significant movement": 0})
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Maps emotions to sentiments
def map_emotion_to_sentiment(emotion):
    emotion_to_sentiment = {
        "happy": "Great event!",
        "sad": "Felt unsafe",
        "neutral": "Amazing experience",
        "angry": "Too crowded",
        "fear": "Too crowded",
        "surprise": "Great event!",
        "disgust": "Too crowded"
    }
    return emotion_to_sentiment.get(emotion, "Neutral sentiment")

# Analyzes facial sentiment using DeepFace
def analyze_facial_sentiment(frame):
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']
        return dominant_emotion
    except Exception as e:
        print(f"Facial sentiment analysis error: {e}")
        return "neutral"

# Analyzes hand gestures using MediaPipe
def analyze_hand_gestures(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        return "Hand movement detected"
    else:
        return "No significant movement"

# Detects anomalies based on hand movement speed
def detect_anomalies(frame):
    global previous_position, anomaly_detected, anomaly_count

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_x = hand_landmarks.landmark[0].x * frame.shape[1]
            wrist_y = hand_landmarks.landmark[0].y * frame.shape[0]
            current_position = (wrist_x, wrist_y)

            if previous_position is not None:
                movement_speed = dist.euclidean(current_position, previous_position)
                if movement_speed > 50:
                    anomaly_detected = True
                    anomaly_count += 1
                    anomaly_times.append(time.time() - start_time)
                else:
                    anomaly_detected = False

            previous_position = current_position

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global cap, anomaly_detected

    while True:
        success, frame = cap.read()
        if not success:
            break

        facial_sentiment = analyze_facial_sentiment(frame)
        hand_behavior = analyze_hand_gestures(frame)
        mapped_sentiment = map_emotion_to_sentiment(facial_sentiment)

        detect_anomalies(frame)

        sentiments_over_time.append(mapped_sentiment)
        behaviors_over_time.append(hand_behavior)
        sentiment_counter[mapped_sentiment] += 1
        behavior_counter[hand_behavior] += 1

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    current_time = time.time() - start_time
    data = {
        "time": current_time,
        "sentiments_over_time": sentiments_over_time,
        "behaviors_over_time": behaviors_over_time,
        "anomaly_times": anomaly_times,
        "anomaly_detected": anomaly_detected
    }
    return jsonify(data)

@app.route('/most_frequent')
def most_frequent():
    most_common_sentiment, highest_count_sentiment = sentiment_counter.most_common(1)[0]
    most_common_behavior, highest_count_behavior = behavior_counter.most_common(1)[0]
    return jsonify({
        "most_common_sentiment": most_common_sentiment,
        "highest_count_sentiment": highest_count_sentiment,
        "most_common_behavior": most_common_behavior,
        "highest_count_behavior": highest_count_behavior
    })

if __name__ == '__main__':
    app.run(debug=True)
