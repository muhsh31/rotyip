import requests

# توكن البوت
BOT_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
# معرف القناة أو المجموعة
CHAT_ID = "-1002612909844"

def send_alert(ip, data, threat_level="High", source="IPQS"):
    """
    يرسل تنبيه إلى تيليغرام عند رصد IP مشبوه
    """
    message = f"""
🚨 <b>IP Alert</b>
<b>IP:</b> {ip}
<b>Country:</b> {data.get("country_code", "-")} 🇺🇸
<b>City:</b> {data.get("city", "-")} 🏙️
<b>Time Zone:</b> {data.get("timezone", "-")} ⏰
"""

    # إضافة ZIP إن وُجد
    if data.get("zipcode", "-") not in ["-", "", None]:
        message += f"<b>ZIP Code:</b> {data.get("zipcode")} 📍\n"

    message += f"<b>Threat Level:</b> {threat_level} ⚠️\n"
    message += f"<b>Score:</b> {data.get("fraud_score", '-')} 🔥"
    
    # إرسال الرسالة
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message.strip(),
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram alert: {e}")
        return False
