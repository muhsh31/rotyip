import requests
from alert_telegram_rotyip import send_alert
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import itertools
import os
import random

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

# دالة استخراج عنوان حقيقي من ZIP
def get_street_address_from_zip(zip_code, country_code="us"):
    try:
        zip_resp = requests.get(f"https://api.zippopotam.us/{country_code}/{zip_code}", timeout=5)
        if zip_resp.status_code != 200:
            return None

        zip_data = zip_resp.json()
        lat = zip_data["places"][0]["latitude"]
        lon = zip_data["places"][0]["longitude"]
        city = zip_data["places"][0]["place name"]
        state = zip_data["places"][0]["state abbreviation"]
        country = zip_data["country"]

        query = f"""
        [out:json];
        way(around:1500,{lat},{lon})["highway"];
        out tags;
        """
        overpass_url = "https://overpass-api.de/api/interpreter"
        resp = requests.post(overpass_url, data={"data": query}, timeout=10)
        if resp.status_code != 200:
            return None

        results = resp.json()
        street_names = list({
            el["tags"]["name"]
            for el in results["elements"]
            if "tags" in el and "name" in el["tags"]
        })

        if not street_names:
            return None

        street = random.choice(street_names)
        number = random.randint(100, 999)
        return f"{number} {street}, {city}, {state} {zip_code}, {country}"

    except Exception as e:
        return None

@app.route("/api/check")
def check_ip():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "Missing IP"}), 400

    if ip in ip_cache:
        return jsonify(ip_cache[ip])

    for _ in range(len(IPQS_KEYS)):
        key = next(KEYS)
        try:
            url = f"https://ipqualityscore.com/api/json/ip/{key}/{ip}"
            response = requests.get(url, timeout=8)
            data = response.json()

            if not data.get("success", True):
                if "limit" in data.get("message", "").lower():
                    send_telegram_message(f"🚫 <b>IPQS API Blocked</b>\nKey ending in ...{key[-4:]}")
                    continue

            score = int(data.get("fraud_score", 0))
            threat_level = "clean"
            if score > 50:
                threat_level = "dangerous"
            elif score > 27:
                threat_level = "suspicious"

            zipcode = data.get("zipcode", "-")

            # ✅ إذا لم يتوفر ZIP من IPQS – استخدم ip-api.com كبديل
            if not zipcode or zipcode == "-":
                try:
                    fallback = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
                    zipcode = fallback.get("zip", "-")
                except:
                    pass

            street_address = get_street_address_from_zip(zipcode)

            result = {
                "ip": ip,
                "country": data.get("country_code", "-"),
                "city": data.get("city", "-"),
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
                "datetime": datetime.utcnow().isoformat(),
                "street_address": street_address or "Not Available"
            }

            ip_cache[ip] = result

            if threat_level in ["suspicious", "dangerous"]:
                send_alert(ip, data, threat_level)

            return jsonify(result)

        except Exception:
            continue

    return jsonify({"error": "All API keys failed"}), 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
