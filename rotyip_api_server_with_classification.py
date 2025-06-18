from flask import Flask, request, jsonify
import sqlite3
import requests
from datetime import datetime

app = Flask(__name__)

DB_PATH = "rotyip_ip_logs.db"

API_KEYS = {
    "ipqs": ["ipqs_key_1", "ipqs_key_2", "ipqs_key_3"]
}

rotators = { "ipqs": 0 }

BOT_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
CHAT_ID = "-1002612909844"

def rotate_key(service):
    keys = API_KEYS[service]
    i = rotators[service]
    key = keys[i]
    rotators[service] = (i + 1) % len(keys)
    return key

def classify_threat(score):
    try:
        score = int(score)
        if score <= 27:
            return "Clean"
        elif 28 <= score <= 50:
            return "Suspicious"
        else:
            return "Dangerous"
    except:
        return "Unknown"

def save_to_db(ip, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ip_logs (ip, country, city, timezone, isp, fraud_score,
                             proxy_type, is_vpn, is_bot, fingerprint, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ip,
        data.get('country'),
        data.get('city'),
        data.get('timezone'),
        data.get('isp'),
        data.get('fraud_score'),
        data.get('proxy_type'),
        data.get('is_vpn', 0),
        data.get('is_bot', 0),
        data.get('fingerprint'),
        data.get('source'),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def send_telegram_alert(ip, threat_level, score, source="IPQS"):
    message = f"🚨 <b>IP Alert</b>\n<b>IP:</b> {ip}\n<b>Threat Level:</b> {threat_level}\n<b>Score:</b> {score}\n<b>Source:</b> {source}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

@app.route('/api/check', methods=['GET'])
def check_ip():
    ip = request.args.get('ip', '')
    if not ip:
        return jsonify({"error": "IP required"}), 400

    key = rotate_key("ipqs")
    try:
        url = f"https://ipqualityscore.com/api/json/ip/{key}/{ip}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            score = data.get("fraud_score", 0)
            threat_label = classify_threat(score)

            result = {
                "ip": ip,
                "country": data.get("country_code"),
                "city": data.get("city"),
                "timezone": data.get("timezone"),
                "isp": data.get("ISP"),
                "fraud_score": score,
                "threat_level": threat_label,
                "proxy_type": data.get("connection_type"),
                "is_vpn": int(data.get("vpn", 0)),
                "is_bot": int(data.get("bot_status", 0)),
                "fingerprint": data.get("device_id"),
                "source": "ipqs"
            }

            save_to_db(ip, result)

            if isinstance(score, int) or (isinstance(score, str) and score.isdigit()):
                score = int(score)
                if score > 27:
                    send_telegram_alert(ip, threat_label, score)

            return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "All services failed"}), 502

if __name__ == '__main__':
    app.run(debug=True)
