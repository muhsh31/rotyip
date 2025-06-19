import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import itertools
import os

app = Flask(__name__)
CORS(app)

# قائمة المفاتيح
IPQS_KEYS = [
    "dgHCQ0L7RO4zy5ER6lqbjIQhQZHIkSw0",
    "D4tu8VKYrdeM9hEVB6z3y3LUldTQhSgH",
    "EfSNh7a0Uvyyg98zyXAqZ8QcxLSm0Rz5",
    "Ty6TTD8QCiJONHbfgSV7w2NvTQClYjRc"
]
KEYS = itertools.cycle(IPQS_KEYS)

# تخزين مؤقت لنتائج الفحص
ip_cache = {}

# إعدادات تيليغرام
TELEGRAM_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
CHAT_ID = "-1002612909844"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=5)
    except:
        pass

@app.route("/api/check")
def check_ip():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "Missing IP"}), 400

    # إذا تم فحص الـ IP مسبقًا، أعد نفس النتيجة
    if ip in ip_cache:
        return jsonify(ip_cache[ip])

    for _ in range(len(IPQS_KEYS)):
        key = next(KEYS)
        try:
            url = f"https://ipqualityscore.com/api/json/ip/{key}/{ip}"
            response = requests.get(url, timeout=8)
            data = response.json()

            # إذا تم حظر المفتاح، أرسل تنبيه وجرب مفتاح آخر
            if not data.get("success", True):
                if "limit" in data.get("message", "").lower():
                    send_telegram_message(f"🚫 <b>IPQS API Blocked</b>\nKey ending in ...{key[-4:]}")
                    continue  # جرّب مفتاحًا آخر

            # تحليل النتيجة
            score = int(data.get("fraud_score", 0))
            threat_level = "clean"
            if score > 50:
                threat_level = "dangerous"
            elif score > 27:
                threat_level = "suspicious"

            result = {
                "ip": ip,
                "country": data.get("country_code", "-"),
                "city": data.get("city", "-"),
                "zipcode": data.get("zipcode", "-"),
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
            }

            # حفظ النتيجة مؤقتًا
            ip_cache[ip] = result

            # إرسال تنبيه عند الخطر
            if threat_level in ["suspicious", "dangerous"]:
                
message = f"""
🚨 <b>IP Alert</b>
<b>IP:</b> {ip}
<b>Country:</b> {data.get("country_code", "-")} 🇺🇸
<b>City:</b> {data.get("city", "-")} 🏙️
<b>Time Zone:</b> {data.get("timezone", "-")} ⏰
"""
if data.get("zipcode", "-") not in ["-", "", None]:
    message += f"<b>ZIP Code:</b> {data.get('zipcode')} 📍\n"
message += f"<b>Threat Level:</b> {threat_level} ⚠️\n"
message += f"<b>Score:</b> {score} 🔥"

send_telegram_message(message.strip())


            return jsonify(result)

        except Exception as e:
            continue  # جرب مفتاح آخر إذا فشل الطلب

    return jsonify({"error": "All API keys failed"}), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
