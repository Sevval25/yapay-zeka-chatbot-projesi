# logger.py
from datetime import datetime

def _log_filename():
    # Günlük bazlı log dosyası
    return f"chat_logs_{datetime.now().strftime('%Y-%m-%d')}.txt"

def log_conversation(user_input: str, response: str, intent: str = None, confidence: float = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = _log_filename()
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"USER: {user_input}\n")
        f.write(f"BOT: {response}\n")
        if intent is not None and confidence is not None:
            f.write(f"INTENT: {intent} (confidence={confidence:.2f})\n")
        f.write("\n")
