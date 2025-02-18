from flask import Flask, request, jsonify
from telethon import TelegramClient

app = Flask(__name__)

# Replace with your own Telegram API ID, API hash, and phone number
API_ID = '23973795'
API_HASH = '207f959c0d1219d40543dfc388de63e0'
PHONE_NUMBER = '+94768515072'
TELEGRAM_CHAT_ID = '5210630997'

client = TelegramClient('session_name', API_ID, API_HASH)

@app.route('/')
def index():
    return "Hello, this is a Telegram message sender!"

@app.route('/send_message', methods=['POST'])
async def send_message():
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        await client.start(phone=PHONE_NUMBER)
        await client.send_message(TELEGRAM_CHAT_ID, message)
        return jsonify({'status': 'Message sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
