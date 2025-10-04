from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    color = os.getenv("APP_COLOR", "blue")
    return f"<h1>Hello from {color.upper()} environment!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
