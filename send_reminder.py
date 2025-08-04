import requests
import os
from datetime import datetime

def generate_daily_message():
    """Generates the daily reminder message based on the day of the week, in the style of Paul Atreides."""
    
    # Get the current day of the week (Monday is 0, Sunday is 6)
    today = datetime.now().weekday()
    
    # Define a dictionary for workout routines
    # Tuesday (1), Thursday (3), and Saturday (5) are workout days
    workout_routines = {
        1: "The Bene Gesserit's test: Chest - Triceps. 🧘‍♂️",
        3: "Forge the warrior: Back, Trapeze, Neck. ⚔️",
        5: "Sharpen the blade: Shoulder - Biceps. ✨"
    }

    # Start with the greeting and daily supplements, which are taken every day
    message_lines = [
        "Heed these words. 🏜️",
        "The path of the day is laid before you. Attend to these directives: 📜"
    ]

    # Add the daily supplements
    message_lines.append("- Consume the water of life; take the collagen shots (10g) before your meal. 💧")
    message_lines.append("- The desert's resolve strengthens with the Tongkat Ali supplement pill after your meal. 💪")

    # Add the workout routine if today is a workout day
    if today in workout_routines:
        message_lines.append(f"- {workout_routines[today]}")

    # Format the final message string
    message = "\n".join(message_lines)
    return message

def send_telegram_message(bot_token, chat_id, message):
    """Sends a message via the Telegram bot."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Message sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return False

def main():
    print("🚀 Starting Telegram reminder...")
    
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print(f"Bot token present: {'Yes' if bot_token else 'No'}")
    print(f"Chat ID present: {'Yes' if chat_id else 'No'}")
    
    if not bot_token or not chat_id:
        print("❌ Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        return
    
    # Generate the daily reminder message
    print("📝 Generating daily message...")
    message = generate_daily_message()
    
    print("📤 Sending message...")
    # Send the message
    success = send_telegram_message(bot_token, chat_id, message)
    
    if success:
        print("✅ Reminder sent successfully!")
    else:
        print("❌ Failed to send reminder!")

if __name__ == "__main__":
    main()
