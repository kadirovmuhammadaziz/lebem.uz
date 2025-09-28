from celery import shared_task
import requests
from django.conf import settings


@shared_task
def send_telegram_notification(message_type, data):
    """Telegram orqali xabar yuborish"""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    if message_type == 'review':
        message = f"""
🌟 <b>Yangi sharh keldi!</b>

👤 <b>Ism:</b> {data['name']}
📱 <b>Telefon:</b> {data['phone']}
🛒 <b>Mahsulot:</b> {data['product']}
⭐ <b>Baho:</b> {data['rating']}/5
💬 <b>Izoh:</b> {data['comment']}

📅 <i>Lebem.uz mebel do'koni</i>
        """
    elif message_type == 'contact':
        message = f"""
📩 <b>Yangi aloqa xabari!</b>

👤 <b>Ism:</b> {data['name']}
📱 <b>Telefon:</b> {data['phone']}
📧 <b>Email:</b> {data.get('email', 'Ko\'rsatilmagan')}
📝 <b>Mavzu:</b> {data['subject']}
💬 <b>Xabar:</b> {data['message']}

📅 <i>Lebem.uz mebel do'koni</i>
        """
    else:
        return False

    payload = {
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False