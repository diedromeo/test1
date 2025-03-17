from flask import Flask
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Squid Game - FTP Challenge</title>
        <style>
            @keyframes blinkCursor {
                50% { border-right-color: transparent; }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            body {
                background-color: black;
                color: lime;
                text-align: center;
                font-family: 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            h1 {
                font-size: 3rem;
                text-shadow: 0px 0px 5px red;
                animation: fadeIn 2s ease-in-out;
            }
            .logo {
                width: 400px;
                margin-bottom: 20px;
                animation: fadeIn 2s ease-in-out;
            }
            .panel {
                border: 2px solid red;
                padding: 20px;
                width: 60%;
                background-color: rgba(255, 0, 0, 0.2);
                animation: fadeIn 2s ease-in-out;
            }
            .typing-container {
                font-size: 1.2rem;
                white-space: nowrap;
                overflow: hidden;
                display: inline-block;
                border-right: 3px solid lime;
                animation: blinkCursor 0.75s step-end infinite;
            }
            .character {
                display: none;
                width: 200px;
                margin-top: 20px;
                animation: fadeIn 2s ease-in-out;
            }
            .hint {
                color: yellow;
                margin-top: 20px;
                animation: fadeIn 3s ease-in-out;
            }
        </style>
    </head>
    <body>
        <img src="https://titanui.com/wp-content/uploads/2021/10/21/Squid-Game-Logo-Vector.jpg" class="logo">
        
        <h1>🔴 Squid Game Secret Panel 🔴</h1>
        
        <div class="panel">
            <p class="typing-container" id="challenge-text"></p>
            <img id="character-img" class="character" src="https://www.pngplay.com/wp-content/uploads/13/Squid-Game-Soldier-Triangle-Cartoon-PNG.png">
            <p class="hint">Hint: Some doors don't require a key, just a username.</p>
            <p class="hint">Connect and retrieve the secret.</p>
        </div>

        <script>
            const text = "Welcome, player! You have entered the Squid Game FTP Challenge. Your goal is simple: find the secret hidden in the system.";
            let i = 0;
            function typeWriter() {
                if (i < text.length) {
                    document.getElementById("challenge-text").innerHTML = text.substring(0, i + 1);
                    i++;
                    setTimeout(typeWriter, 50); // Smooth typing speed
                } else {
                    document.getElementById("challenge-text").style.borderRight = "none"; // Remove cursor after typing
                    document.getElementById("character-img").style.display = "block"; // Show character
                }
            }
            window.onload = typeWriter;
        </script>
    </body>
    </html>
    """

# Function to start the FTP server
def start_ftp():
    os.makedirs("/tmp/ftp_root", exist_ok=True)
    
    # Create the flag file inside the FTP server directory
    with open("/tmp/ftp_root/flag.txt", "w") as f:
        f.write("CyberX{F7P_H@CKER}\n")

    authorizer = DummyAuthorizer()
    authorizer.add_anonymous("/tmp/ftp_root")  # Allow anonymous login

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

# Run FTP server in a separate thread
ftp_thread = Thread(target=start_ftp, daemon=True)
ftp_thread.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
