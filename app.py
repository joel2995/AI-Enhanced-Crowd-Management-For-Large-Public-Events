from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)

# Video capture
video_path = 'C:\Users\user\OneDrive\Desktop\Hackathon Projects\CCTV Analysis\4196258-hd_1280_720_30fps.mp4'
cap = cv2.VideoCapture(video_path)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_people_count')
def get_people_count():
    try:
        with open('people_count.txt', 'r') as f:
            count = f.read().strip()
    except FileNotFoundError:
        count = '0'
    return jsonify({'count': int(count)})

if __name__ == '__main__':
    app.run(debug=True)
