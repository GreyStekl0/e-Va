from flask import Flask, request, render_template, jsonify, request, send_file, render_template

import requests
import io
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


@app.route('/download', methods=['POST'])
def download():
    texts = request.form.getlist('text')
    combined_text = f"<{'\n'.join(texts)}\n>"
    print(combined_text)
    binary_data = combined_text.encode('utf-8')
    return send_file(
        io.BytesIO(binary_data),
        as_attachment=True,
        download_name='e-va_card.bin',
        mimetype='application/octet-stream'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
