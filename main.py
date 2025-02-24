import os
import logging
import telebot
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", 8558))
CHAT_ID = os.getenv("CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL is not set in environment variables")

dbot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

dbot.remove_webhook()
dbot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
logging.info(f"Webhook set to {WEBHOOK_URL}/webhook")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        status = data.get("status", "Unknown")
        name = data.get("name", "Unknown")
        description = data.get("description", "No description")

        message = f"\U0001F6A8 *Health Check Alert!*\n\n"
        message += f"*Service:* {name}\n"
        message += f"*Status:* {status}\n"
        message += f"*Description:* {description}"

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
