import base64
import json
import os
import logging
from flask import Flask, request
from google.cloud import language_v1, secretmanager
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Slack secret dynamically
def get_slack_token():
    secret_name = os.environ.get("SLACK_SECRET_PATH", "projects/1046723826220/secrets/slacktoken/versions/latest")
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")

# Sentiment analysis
def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment.score

# Slack message sender
def send_to_slack(channel, message):
    slack_token = get_slack_token()
    headers = {"Authorization": f"Bearer {slack_token}"}
    payload = {"channel": channel, "text": message}

    response = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    logger.info(f"Slack response: {response.text}")

    if not response.ok or not response.json().get("ok", False):
        raise Exception(f"Failed to post to Slack: {response.text}")

# Pub/Sub handler
@app.route("/", methods=["POST"])
def handle_pubsub():
    envelope = request.get_json()
    if not envelope or 'message' not in envelope or 'data' not in envelope['message']:
        return "Bad Request: Missing Pub/Sub message", 400

    try:
        msg_data = base64.b64decode(envelope['message']['data']).decode('utf-8')
        data = json.loads(msg_data)

        if 'user_id' not in data or 'message' not in data:
            return "Bad Request: Missing user_id or message", 400

        sentiment_score = analyze_sentiment(data["message"])
        logger.info(f"Sentiment score: {sentiment_score}")

        if sentiment_score < 0:
            logger.info("Negative sentiment detected — sending to Slack.")
            send_to_slack("#support", f"⚠️ Negative feedback from {data['user_id']}: {data['message']}")

        return "", 204

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return "Internal Server Error", 500

# Entry point for local testing or Cloud Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
