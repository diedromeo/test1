from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
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
            width: 90vw;
            max-width: 500px;
            height: 50vh;
            max-height: 300px;
            border: 4px solid #ff0055;
            box-shadow: 0 0 15px #ff0055;
            margin: 20px auto;
            overflow: hidden;
            border-radius: 10px;
        }

        #flag {
            position: absolute;
            width: 60px;
            height: 60px;
            background: url('https://i.pinimg.com/564x/07/44/fc/0744fcfcfba6032880e412d40513877b.jpg') no-repeat center/cover;
            background-size: contain;
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
    <p>Catch the flag if you can! It moves when you get close!</p>

    <div id="game-container">
        <div id="flag"></div>
    </div>

    <button class="btn" onclick="revealHint()">Need a Hint?</button>

    <p id="hint"> You should learn HTML CSS JS NOOB ...</p>

    <p id="win-text">🎉 YOU CAUGHT IT! 🎉</p>

    <script>
        let flag = document.getElementById("flag");
        let gameContainer = document.getElementById("game-container");
        let winText = document.getElementById("win-text");
        let moving = true;
        let caughtCount = 0;

        function moveFlag() {
            if (moving) {
                let x = Math.random() * (gameContainer.clientWidth - flag.clientWidth);
                let y = Math.random() * (gameContainer.clientHeight - flag.clientHeight);
                flag.style.transform = `translate(${x}px, ${y}px)`;
            }
        }

        flag.addEventListener("mouseenter", moveFlag); // Moves when hovered

        flag.addEventListener("click", function() {
            moving = false; // Stop movement on click
            caughtCount += 1;
            winText.innerHTML = `🎉 YOU CAUGHT IT ${caughtCount} TIME${caughtCount > 1 ? 'S' : ''}! 🎉`;
            winText.style.display = "block";
            alert(`HOW?! 😱\\nHere is your flag:\\CyberX{R3al_C7F_7}`);
        });

        console.log("%c🦑 Squid Game Hint: Type stopFlag() in the console to freeze the flag!", 
            "color: red; font-size: 16px; font-weight: bold;");

        function stopFlag() {
            moving = false;
            console.log("🔴 Red Light! Flag movement stopped.");
        }

        function revealHint() {
            document.getElementById("hint").style.display = "block";
        }
    </script>

</body>
</html>
    """

if __name__ == "__main__":
    app.run(debug=True)
