import requests
import os
from datetime import date

# --- CONFIGURATION (Cycle Settings) ---
ON_DAYS = 5
OFF_DAYS = 2
WEEKLY_CYCLE = ON_DAYS + OFF_DAYS
ACTIVE_DAYS = 56      # 8 weeks
LONG_BREAK_DAYS = 14  # 2 weeks
FULL_CYCLE = ACTIVE_DAYS + LONG_BREAK_DAYS  # 70 days

def generate_daily_message():
    """Generates the daily message based on the Tongkat Ali cycle."""
    
    # 1. Get Start Date (Environment Variable or Default)
    # If TONGKAT_START_DATE is not set in GitHub Secrets, it uses the default below.
    start_date_str = os.getenv("TONGKAT_START_DATE", "2025-12-17")
    
    try:
        start_date = date.fromisoformat(start_date_str)
    except ValueError:
        return "⚠️ ERROR: Invalid date format (must be YYYY-MM-DD)."

    today = date.today()
    days_passed = (today - start_date).days

    # Debug logs (Visible in GitHub Actions console)
    print(f"📅 Start Date: {start_date}")
    print(f"📅 Today: {today}")
    print(f"🔢 Days Passed: {days_passed}")

    # If the cycle hasn't started yet
    if days_passed < 0:
        return f"⏳ Cycle hasn't started yet. ({abs(days_passed)} days left)"

    cycle_day = days_passed % FULL_CYCLE
    print(f"🔄 Cycle Day (0-69): {cycle_day}")

    # 🔵 Long break (2 weeks) - From day 56 to 69
    if cycle_day >= ACTIVE_DAYS:
        return "Let your body fully reset 🔵 (Long Break)"
    
    # 🟢 Weekly 5 ON / 2 OFF
    weekly_day = cycle_day % WEEKLY_CYCLE
    if weekly_day < ON_DAYS:
        return "T Maxxing 🟢"
    else:
        return "Let your body rest"

def send_telegram_message(bot_token, chat_id, message):
    """Sends the message via Telegram API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print(f"📤 Message sent to API. Response code: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    print("🚀 Starting Tongkat Ali Reminder...")
    
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Security check (Do not print the token, just check existence)
    print(f"Bot token present: {'Yes' if bot_token else 'No'}")
    print(f"Chat ID present: {'Yes' if chat_id else 'No'}")
    
    if not bot_token or not chat_id:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set!")
        return
    
    # Generate the message
    print("📝 Calculating daily message...")
    message = generate_daily_message()
    print(f"💬 Message to send: {message}")
    
    # Send the message
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("✅ Process completed successfully!")
    else:
        print("❌ Process failed!")
        # Optional: exit(1) to notify GitHub Actions of failure

if __name__ == "__main__":
    main()
