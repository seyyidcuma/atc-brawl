import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Render'a kaydettiğimiz Telegram Bot Token'ı buraya otomatik gelecek
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def home():
    return "ATC Brawl Server is running successfully!"

# Oyuncunun Telegram'a doğrulama kodu istemesi için endpoint
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    chat_id = data.get('chat_id')
    code = data.get('code', '1234')
    
    if not chat_id:
        return jsonify({"status": "error", "message": "Chat ID not found"}), 400
        
    message = f"ATC Brawl Onay Kodunuz: {code}. Oyuna girerken bunu kullanın!"
    
    # Telegram'a mesajı gönder
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(TELEGRAM_API_URL, json=payload)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Code sent to Telegram!"})
    else:
        return jsonify({"status": "error", "message": "Failed to send Telegram message"}), 500

if __name__ == '__main__':
    # Render'ın verdiği port üzerinden başlatıyoruz
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
