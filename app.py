from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.json
    recipient = data.get("to")
    message = data.get("message")

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": { "body": message }
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/")
def home():
    return "WhatsApp Flask API is running."

@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        # Verification challenge
        verify_token = os.environ.get("VERIFY_TOKEN", "my_verify_token")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            print("Webhook verified")
            return challenge, 200
        else:
            return "Verification failed", 403

    if request.method == "POST":
        data = request.get_json()
        print("Incoming webhook data:", data)
        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

