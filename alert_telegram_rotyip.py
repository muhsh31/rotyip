import requests

# إعدادات التلغرام
BOT_TOKEN = "7682246390:AAFRw4n3DA8FPjmfPs3ndo6OrUlIWR4Odg0"
CHAT_ID = "-1002612909844"

def send_alert(ip, threat_level="High", source="IPQS"):
    message = f"🚨 <b>IP Alert</b>\n<b>IP:</b> {ip}\n<b>Threat Level:</b> {threat_level}\n<b>Source:</b> {source}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)
    return response.json()

# تجربة يدوية
if __name__ == "__main__":
    print(send_alert("8.8.8.8", "Suspicious", "IPQualityScore"))
