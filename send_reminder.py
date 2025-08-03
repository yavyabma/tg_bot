# send_reminder.py
import requests
import os
from datetime import datetime

def read_daily_tasks():
    """Read tasks from a text file"""
    try:
        with open('daily_tasks.txt', 'r', encoding='utf-8') as file:
            tasks = file.read().strip()
            if tasks:
                return tasks
            else:
                return "No tasks scheduled for today! 🎉"
    except FileNotFoundError:
        return "Task file not found. Please create 'daily_tasks.txt' with your daily tasks."

def send_telegram_message(bot_token, chat_id, message):
    """Send message via Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
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
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set")
        return
    
    # Read daily tasks
    tasks = read_daily_tasks()
    
    # Format the message
    today = datetime.now().strftime("%A, %B %d, %Y")
    message = f"""🌅 *Good Morning!*
    
📅 *{today}*

📝 *Today's Tasks:*
{tasks}

Have a productive day! ✨"""
    
    # Send the message
    send_telegram_message(bot_token, chat_id, message)

if __name__ == "__main__":
    main()