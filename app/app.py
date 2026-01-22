from flask import Flask, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello from Flask CI/CD via Jenkins & Docker. Created at {datetime.now()}"

@app.route("/health")
def health():
    # return f"Hello health status ok. Created at {datetime.now()}"
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
