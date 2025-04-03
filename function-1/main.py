
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import os, json

app = Flask(__name__)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("GCP_PROJECT"), "feedback-topic")

@app.route("/", methods=["POST"])
def receive_feedback():
    data = request.get_json()
    if not data or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    
    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    return jsonify({"status": "Message published"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
