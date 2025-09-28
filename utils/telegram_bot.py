import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_message_to_telegram(chat_id, message):
    """Telegram botga xabar yuborish"""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("Telegram bot token o'rnatilmagan")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Telegram yuborishda xato: {e}")
        return False


def send_review_to_telegram(review):
    """Foydalanuvchiga izoh tasdiqlash xabarini yuborish"""
    message = f"""
🎉 <b>Izohingiz qabul qilindi!</b>

📝 <b>Mahsulot:</b> {review.product.name}
👤 <b>Ism:</b> {review.name}
💬 <b>Izoh:</b> {review.comment}

Tez orada siz bilan bog'lanamiz!
    """

    # Bu yerda foydalanuvchining chat_id si bo'lishi kerak
    # Hozircha faqat admin chat_id ga yuborish
    return send_message_to_telegram(settings.ADMIN_CHAT_ID, message)


def send_review_to_admin(review):
    """Adminga yangi izoh haqida xabar yuborish"""
    message = f"""
🔔 <b>Yangi izoh keldi!</b>

📝 <b>Mahsulot:</b> {review.product.name}
👤 <b>Ism:</b> {review.name}
📞 <b>Telefon:</b> {review.phone}
💬 <b>Izoh:</b> {review.comment}
📅 <b>Sana:</b> {review.created_at.strftime('%d.%m.%Y %H:%M')}

Admin paneliga kirish: /admin/
    """

    return send_message_to_telegram(settings.ADMIN_CHAT_ID, message)


