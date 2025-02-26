import os
import logging
import telebot
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", 8558))
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN or CHAT_ID is not set in environment variables")

dbot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/unhealthy", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        status = data.get("status", "Unknown Status")
        description = data.get("description", "No details available")

        message = f"\U0001F6A8 *Incidents Health Check Alert!*\n\n"
        message += f"*Status:* {status}\n"
        message += f"*Description:* {description}\n"

        dbot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        logging.info(f"Sent message: {message}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def run_bot():
    app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run_bot()
