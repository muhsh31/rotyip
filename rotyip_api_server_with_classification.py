import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

IPQS_KEY = "dgHCQ0L7RO4zy5ER6lqbjIQhQZHIkSw0"
TELEGRAM_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
CHAT_ID = "-1002612909844"

def send_telegram_alert(ip, country, city, zip_code, threat_level, score):
    message = f"🚨 <b>IP Alert</b>\n"
    message += f"<b>IP:</b> {ip}\n"
    message += f"<b>Country:</b> {country}\n"
    message += f"<b>City:</b> {city}\n"
    message += f"<b>ZIP:</b> {zip_code}\n"
    message += f"<b>Threat Level:</b> {threat_level}\n"
    message += f"<b>Fraud Score:</b> {score}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print("Telegram error:", e)

@app.route("/api/check")
def check_ip():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "Missing IP"}), 400

    try:
        url = f"https://ipqualityscore.com/api/json/ip/{IPQS_KEY}/{ip}"
        response = requests.get(url, timeout=8)
        data = response.json()

        score = int(data.get("fraud_score", 0))
        threat_level = "clean"
        if score > 50:
            threat_level = "dangerous"
        elif score > 27:
            threat_level = "suspicious"

        country = data.get("country_code", "-")
        city = data.get("city", "-")
        zipcode = data.get("zipcode", "-")

        # إرسال تنبيه عند وجود خطر أو شك
        if threat_level in ["suspicious", "dangerous"]:
            send_telegram_alert(ip, country, city, zipcode, threat_level, score)

        return jsonify({
            "ip": ip,
            "country": country,
            "city": city,
            "zipcode": zipcode,
            "timezone": data.get("timezone", "-"),
            "isp": data.get("ISP", "-"),
            "threat_level": threat_level,
            "fraud_score": score,
            "proxy": data.get("proxy", False),
            "vpn": data.get("vpn", False),
            "tor": data.get("tor", False),
            "connection_type": data.get("connection_type", "-"),
            "organization": data.get("organization", "-"),
            "datetime": datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
