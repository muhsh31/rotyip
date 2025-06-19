import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

IPQS_KEY = "dgHCQ0L7RO4zy5ER6lqbjIQhQZHIkSw0"

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
        elif score > 25:
            threat_level = "suspicious"

        return jsonify({
            "ip": ip,
            "country": data.get("country_code", "-"),
            "city": data.get("city", "-"),
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
