from flask import Flask, request, render_template, jsonify
import requests

from config import bot_token, chat_id

app = Flask(__name__)

# Telegram Bot token and chat ID
BOT_TOKEN = bot_token
CHAT_ID = chat_id


# Helper function to send messages to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        if not data.get("ok"):  # Check if the Telegram API reports success
            print(f"Telegram API error: {data}")
            return False

        print(f"Message sent successfully: {data}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error during Telegram API request: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/constructor')
def constructor():
    return render_template('constructor.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/order', methods=['POST'])
def order():
    try:
        # Extract data from form
        design = request.form.get('design')
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Validate form data
        if not all([design, name, phone, email]):
            return jsonify({"error": "All fields are required."}), 400

        # Format message for Telegram
        message = (
            f"Новый заказ:\n"
            f"Дизайн: {design}\n"
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Email: {email}"
        )

        # Send message to Telegram
        if not send_to_telegram(message):
            return jsonify({"error": "Failed to send message to Telegram."}), 500

        return jsonify({"success": True}), 200

    except Exception as e:
        print(f"Error processing order: {e}")
        return jsonify({"error": "An internal error occurred."}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)