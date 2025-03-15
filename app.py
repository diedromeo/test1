from flask import Flask, render_template, request
import random

app = Flask(__name__)

def is_mobile():
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_indicators = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'opera mini', 'blackberry', 'windows phone']
    desktop_indicators = ['windows', 'macintosh', 'linux', 'x11']
    
    if any(mobile in user_agent for mobile in mobile_indicators) and not any(desktop in user_agent for desktop in desktop_indicators):
        return True
    return False

@app.route('/')
def index():
    if is_mobile():
        return """
        <html><body style="background-color:black; color:red; text-align:center;">
        <h1>🚫 ACCESS DENIED 🚫</h1>
        <p>Your device is not supported.</p>
        <p>Tip: Try learning <b>HTML, CSS, JS</b> first! 😉</p>
        </body></html>
        """
    
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Squid Game CTF - Catch the Flag</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Squada+One&display=swap');

        body {
            margin: 0;
            padding: 0;
            background-color: black;
            color: white;
            font-family: 'Squada One', cursive;
            text-align: center;
            overflow: hidden;
        }

        #logo {
            width: 150px;
            margin: 20px auto;
            display: block;
        }

        #game-container {
            position: relative;
            width: 95vw;
            max-width: 800px;
            height: 70vh;
            max-height: 500px;
            border: 4px solid #ff0055;
            box-shadow: 0 0 15px #ff0055;
            margin: 20px auto;
            overflow: hidden;
            border-radius: 10px;
        }

        .flag {
            position: absolute;
            width: 60px;
            height: 60px;
            background: url('https://i.pinimg.com/564x/07/44/fc/0744fcfcfba6032880e412d40513877b.jpg') no-repeat center/cover;
            cursor: pointer;
        }

        h1 {
            font-size: 2.5rem;
            color: #ff0055;
            text-shadow: 0 0 10px #ff0055;
        }

        .btn {
            margin-top: 10px;
            padding: 12px 24px;
            font-size: 1.2rem;
            background: linear-gradient(135deg, #ff0055, #ff3377);
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: 0.3s ease;
            box-shadow: 0 0 10px rgba(255, 0, 85, 0.8);
        }

        .btn:hover {
            transform: scale(1.1);
            background: linear-gradient(135deg, #ff3377, #ff0055);
        }

        #hint {
            display: none;
            color: yellow;
            font-size: 1.3rem;
            margin-top: 15px;
        }

        #win-text {
            display: none;
            font-size: 2rem;
            color: lime;
            margin-top: 20px;
            animation: blink 1s infinite alternate;
        }

        @keyframes blink {
            from { opacity: 1; }
            to { opacity: 0.3; }
        }
    </style>
</head>
<body>

    <img id="logo" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSA2iJXn4HxB-MTbxOx1wh_FZHlhP5dsDyUQw&s" alt="Squid Game Logo">

    <h1>🦑 Squid Game CTF Challenge</h1>
    <p>Catch the flag if you can! It moves constantly!</p>

    <div id="game-container">
        <div id="flag" class="flag"></div>
    </div>

    <button class="btn" onclick="revealHint()">Need a Hint?</button>

    <p id="hint"> Learn HTML, CSS, JS, NOOB ...</p>

    <p id="win-text">🎉 YOU CAUGHT IT! 🎉</p>

    <script>
        let flag = document.getElementById("flag");
        let gameContainer = document.getElementById("game-container");
        let winText = document.getElementById("win-text");
        let fakeFlags = [];
        
        function moveFlag() {
            let x = Math.random() * (gameContainer.clientWidth - flag.clientWidth);
            let y = Math.random() * (gameContainer.clientHeight - flag.clientHeight);
            flag.style.transform = `translate(${x}px, ${y}px)`;
        }

        function moveFakeFlags() {
            fakeFlags.forEach(fakeFlag => {
                let x = Math.random() * (gameContainer.clientWidth - 60);
                let y = Math.random() * (gameContainer.clientHeight - 60);
                fakeFlag.style.transform = `translate(${x}px, ${y}px)`;
            });
        }

        function createFakeFlags() {
            for (let i = 0; i < 6; i++) {
                let fakeFlag = document.createElement("div");
                fakeFlag.className = "flag";
                gameContainer.appendChild(fakeFlag);
                fakeFlags.push(fakeFlag);
            }
            setInterval(moveFakeFlags, 250);
        }

        setInterval(moveFlag, 200);

        flag.addEventListener("click", function() {
            winText.style.display = "block";
            alert(`HOW?! 😱\nHere is your flag:\\CyberX{Impossible_Capture}`);
        });

        function revealHint() {
            document.getElementById("hint").style.display = "block";
        }
    </script>
</body>
</html>
    """

if __name__ == '__main__':
    app.run(debug=True)
