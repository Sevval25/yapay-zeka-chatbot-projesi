from constants import INFO_MAP

def decide_action(intent: str, confidence: float) -> str:
    if intent in INFO_MAP:
        return intent  # rule tabanı
    return "use_gpt"  # fallback GPT
