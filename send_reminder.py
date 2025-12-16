import requests
import os
from datetime import date

# --- KONFİGÜRASYON (Döngü Ayarları) ---
ON_DAYS = 5
OFF_DAYS = 2
WEEKLY_CYCLE = ON_DAYS + OFF_DAYS
ACTIVE_DAYS = 56      # 8 hafta
LONG_BREAK_DAYS = 14  # 2 hafta
FULL_CYCLE = ACTIVE_DAYS + LONG_BREAK_DAYS  # 70 gün

def generate_daily_message():
    """Tongkat Ali döngüsüne göre günlük mesajı oluşturur."""
    
    # 1. Başlangıç Tarihini Al (Environment Variable veya Sabit Tarih)
    # GitHub Secrets'a TONGKAT_START_DATE eklemezsen buradaki tarihi baz alır.
    start_date_str = os.getenv("TONGKAT_START_DATE", "2025-12-17")
    
    try:
        start_date = date.fromisoformat(start_date_str)
    except ValueError:
        return "⚠️ HATA: Tarih formatı geçersiz (YYYY-MM-DD olmalı)."

    today = date.today()
    days_passed = (today - start_date).days

    # Debug için log (GitHub Actions konsolunda görünür)
    print(f"📅 Start Date: {start_date}")
    print(f"📅 Today: {today}")
    print(f"🔢 Days Passed: {days_passed}")

    # Döngü henüz başlamadıysa
    if days_passed < 0:
        return f"⏳ Döngü başlamadı. ({abs(days_passed)} gün kaldı)"

    cycle_day = days_passed % FULL_CYCLE
    print(f"🔄 Cycle Day (0-69): {cycle_day}")

    # 🔵 Long break (2 weeks)
    if cycle_day >= ACTIVE_DAYS:
        return "Let your body fully reset 🔵 (Long Break)"
    
    # 🟢 Weekly 5 ON / 2 OFF
    weekly_day = cycle_day % WEEKLY_CYCLE
    if weekly_day < ON_DAYS:
        return "T Maxxing 🟢 (ON Day)"
    else:
        return "Let your body rest 🟡 (OFF Day)"

def send_telegram_message(bot_token, chat_id, message):
    """Telegram mesajını gönderir."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print(f"📤 Mesaj API'ye iletildi. Response: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Mesaj gönderme hatası: {e}")
        return False

def main():
    print("🚀 Tongkat Ali Reminder başlatılıyor...")
    
    # Environment değişkenlerini al
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Güvenlik kontrolü (Loglarda token görünmez, sadece var/yok yazar)
    print(f"Bot token mevcut: {'Evet' if bot_token else 'Hayır'}")
    print(f"Chat ID mevcut: {'Evet' if chat_id else 'Hayır'}")
    
    if not bot_token or not chat_id:
        print("❌ HATA: TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID ayarlanmalı!")
        return
    
    # Mesajı oluştur
    print("📝 Günlük mesaj hesaplanıyor...")
    message = generate_daily_message()
    print(f"💬 Gönderilecek Mesaj: {message}")
    
    # Gönder
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("✅ İşlem başarıyla tamamlandı!")
    else:
        print("❌ İşlem başarısız oldu!")
        # GitHub Actions'ın hatayı fark etmesi için exit code 1 verilebilir (opsiyonel)
        # exit(1) 

if __name__ == "__main__":
    main()
