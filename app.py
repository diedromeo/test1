from flask import Flask, render_template, request

app = Flask(__name__)

def decode(x):
    if x == "minuteman kang":
        f = "byteme{infiltrated_tva_successfully}"
        return f
    else:
        return "A god doesn't PLEAD!! Try again."

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        password = request.form.get('password', '')
        message = decode(password)
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
