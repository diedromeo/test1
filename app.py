from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import requests
import threading

app = Flask(__name__)

# Load Haarcascade for Face Detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load Pre-Trained Full Body Detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

camera = cv2.VideoCapture(0)
background_subtractor = cv2.createBackgroundSubtractorMOG2()

alert_message = ""
last_alert = ""

# Telegram Bot Credentials (Replace with your details)
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

def send_telegram_alert(message):
    """Send alert message to Telegram"""
    global last_alert
    if message != last_alert:  # Prevent spamming
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url)
        last_alert = message

def detect_employee():
    global alert_message
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Improve motion detection
        fg_mask = background_subtractor.apply(gray)
        fg_mask = cv2.erode(fg_mask, None, iterations=2)  # Remove noise
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)  # Fill gaps

        # Detect standing (using body detection instead of simple motion)
        bodies, _ = hog.detectMultiScale(frame, winStride=(8,8), padding=(8,8), scale=1.05)
        if len(bodies) > 0:
            alert_message = "<span style='color: red;'>🚨 Employee is standing! 🚨</span>"
            threading.Thread(target=send_telegram_alert, args=("🚨 Employee is standing! 🚨",)).start()
        else:
            alert_message = ""

        # Detect faces (Phone usage)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle
            alert_message = "<span style='color: red;'>📱🚨 Employee using phone! 🚨</span>"
            threading.Thread(target=send_telegram_alert, args=("📱🚨 Employee using phone! 🚨",)).start()

        # Draw body detections (Standing alert)
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle

        # Convert frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Employee Monitoring</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #111; color: lime; }
            h1 { color: lime; }
            .alert { font-size: 20px; margin-top: 10px; font-weight: bold; }
        </style>
        <script>
            function checkAlert() {
                fetch('/alert').then(response => response.json()).then(data => {
                    document.getElementById('alert-box').innerHTML = data.alert;
                });
            }
            setInterval(checkAlert, 1000);
        </script>
    </head>
    <body>
        <h1>Employee Monitoring System</h1>
        <img src="/video_feed" width="640" height="480">
        <div id="alert-box" class="alert"></div>
    </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    return Response(detect_employee(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alert')
def alert():
    return jsonify({"alert": alert_message})

if __name__ == '__main__':
    app.run(debug=True)
