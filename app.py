from flask import Flask, request, jsonify
from telethon import TelegramClient, sync
import requests

app = Flask(__name__)

# Replace with your own Telegram API ID, API hash, and phone number
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'
TELEGRAM_CHAT_ID = 'YOUR_TELEGRAM_CHAT_ID'

client = TelegramClient('session_name', API_ID, API_HASH)
client.start(phone=PHONE_NUMBER)

@app.route('/')
def index():
    return "Welcome to the Random Joke Generator!"

@app.route('/random_joke', methods=['GET'])
def random_joke():
    JOKE_API_URL = 'https://v2.jokeapi.dev/joke/Any'
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()
        joke_data = response.json()

        if joke_data['type'] == 'single':
            joke = joke_data['joke']
        else:
            joke = f"{joke_data['setup']} - {joke_data['delivery']}"

        return jsonify({'joke': joke}), 200
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        with client:
            client.loop.run_until_complete(client.send_message(TELEGRAM_CHAT_ID, message))
        return jsonify({'status': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
