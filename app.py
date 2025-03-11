from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import requests

app = Flask(__name__)

# Load Haarcascade for Face Detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load Pre-Trained Full Body Detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

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

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Monitoring</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #111; color: lime; }
            h1 { color: lime; }
            video { width: 640px; height: 480px; border: 2px solid lime; margin-top: 20px; display: none; }
            .alert { font-size: 20px; margin-top: 10px; font-weight: bold; }
            button { background-color: lime; color: black; padding: 10px 20px; font-size: 18px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Employee Monitoring System</h1>
        <button id="start-btn">Allow Camera Access</button>
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas" style="display: none;"></canvas>
        <div id="alert-box" class="alert"></div>

        <script>
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const startBtn = document.getElementById('start-btn');

            // Ask for camera access when button is clicked
            startBtn.addEventListener('click', function () {
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        video.srcObject = stream;
                        video.style.display = "block";  // Show video
                        startBtn.style.display = "none";  // Hide button after permission
                        setInterval(sendFrame, 1000);  // Start sending frames
                    })
                    .catch(err => {
                        alert("Camera access denied! Please allow camera access.");
                        console.error("Error accessing camera: ", err);
                    });
            });

            function sendFrame() {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                let imageData = canvas.toDataURL('image/jpeg');  // Convert frame to Base64

                fetch('/process_frame', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imageData })
                }).then(response => response.json())
                  .then(data => {
                      document.getElementById('alert-box').innerHTML = data.alert;
                  });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/process_frame', methods=['POST'])
def process_frame():
    global alert_message

    # Get image from request
    data = request.json['image']
    img_data = base64.b64decode(data.split(',')[1])  # Convert Base64 to bytes
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Background subtraction (Motion detection)
    fg_mask = background_subtractor.apply(gray)
    fg_mask = cv2.erode(fg_mask, None, iterations=2)
    fg_mask = cv2.dilate(fg_mask, None, iterations=2)

    # Detect standing people
    bodies, _ = hog.detectMultiScale(frame, winStride=(8,8), padding=(8,8), scale=1.05)
    if len(bodies) > 0:
        alert_message = "<span style='color: red;'>🚨 Employee is standing! 🚨</span>"
        send_telegram_alert("🚨 Employee is standing! 🚨")
    else:
        alert_message = ""

    # Detect faces (Phone usage)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        alert_message = "<span style='color: red;'>📱🚨 Employee using phone! 🚨</span>"
        send_telegram_alert("📱🚨 Employee using phone! 🚨")

    return jsonify({"alert": alert_message})

if __name__ == '__main__':
    app.run(debug=True)
