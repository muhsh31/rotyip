import requests
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)
CORS(app)

TELEGRAM_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
CHAT_ID = "-1002612909844"

def check_scamalytics(ip):
    try:
        url = f"https://scamalytics.com/ip/{ip}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        score_section = soup.find("div", class_="score-card")
        threat_score = "-"
        if score_section:
            threat_score = score_section.text.strip().split()[0]

        details = soup.find("table", class_="table")
        flags = []
        if details:
            for row in details.find_all("tr"):
                tds = row.find_all("td")
                if len(tds) == 2:
                    label = tds[0].text.strip()
                    value = tds[1].text.strip()
                    flags.append(f"{label}: {value}")

        return {
            "threat_score": threat_score,
            "flags": flags
        }
    except Exception as e:
        return {"error": str(e)}

def send_telegram(ip, level):
    msg = f"🚨 <b>IP Alert</b>\n<b>IP:</b> {ip}\n<b>Threat:</b> {level}\n<b>Source:</b> Scamalytics"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except:
        pass

@app.route("/api/check")
def check_ip():
    ip = request.args.get("ip", "").strip()
    if not ip:
        return jsonify({"error": "Missing IP"}), 400

    result = check_scamalytics(ip)

    threat = result.get("threat_score", "-")
    threat_level = "clean"
    if threat != "-" and threat != "0":
        score = int(threat)
        if score >= 50:
            threat_level = "dangerous"
        elif score >= 25:
            threat_level = "suspicious"

    # إرسال تيليغرام عند الخطر
    if threat_level in ["suspicious", "dangerous"]:
        send_telegram(ip, threat_level)

    return jsonify({
        "ip": ip,
        "source": "scamalytics",
        "checked_at": datetime.utcnow().isoformat(),
        "threat_score": threat,
        "threat_level": threat_level,
        "flags": result.get("flags", [])
    })

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
