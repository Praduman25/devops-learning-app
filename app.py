from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello! This is my first DevOps learning app.")

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)