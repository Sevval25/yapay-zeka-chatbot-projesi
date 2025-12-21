from datetime import datetime

LOG_FILE = "chat_logs.txt"

def log_conversation(user_input, response):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}]\n")
        f.write(f"USER: {user_input}\n")
        f.write(f"BOT: {response}\n\n")
