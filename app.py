from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import requests

app = Flask(__name__)

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
        <button id="start-btn">Start Camera</button>
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas" style="display: none;"></canvas>
        <div id="alert-box" class="alert"></div>

        <script>
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            const startBtn = document.getElementById('start-btn');

            // Ensure camera permission is requested
            startBtn.addEventListener('click', async function () {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    video.style.display = "block"; // Show video
                    startBtn.style.display = "none"; // Hide button
                    setInterval(sendFrame, 1000); // Start sending frames
                } catch (err) {
                    alert("⚠️ Camera access denied! Please allow camera access in browser settings.");
                    console.error("Error accessing camera: ", err);
                }
            });

            function sendFrame() {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                let imageData = canvas.toDataURL('image/jpeg'); // Convert frame to Base64

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
    return jsonify({"alert": "✅ Camera is working!"})

if __name__ == '__main__':
    app.run(debug=True)
