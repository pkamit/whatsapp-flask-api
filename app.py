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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

