# dialog_manager.py
from constants import INFO_MAP

# Güven eşiğini biraz yüksek tutalım ki bot emin olmadan konuşmasın.
CONFIDENCE_THRESHOLD = 0.60


def decide_action(intent: str, confidence: float) -> str:
    """
    BERT'ten gelen intent ve skora göre ne yapacağımıza karar verir.
    Dönüş Değeri: 'shipping', 'discount' gibi bir anahtar kelime VEYA 'fallback'.
    """

    # 1. Eğer step2_nlu.py zaten "fallback" dediyse (kural veya hata)
    if intent == "fallback":
        return "fallback"

    # 2. Model bir şey buldu ama güveni düşükse
    if confidence < CONFIDENCE_THRESHOLD:
        print(f"⚠️ Güven düşük ({confidence:.2f} < {CONFIDENCE_THRESHOLD}). Fallback'e gidiliyor.")
        return "fallback"

    # 3. Modelin bulduğu intent bizim cevap anahtarımızda (INFO_MAP) var mı?
    if intent in INFO_MAP:
        return intent

    # 4. Tanımsız durum (Listede olmayan bir şey gelirse)
    return "fallback"


def get_static_response(action: str) -> str:
    """
    Karar verilen action'a göre INFO_MAP'ten metni çeker.
    Eğer action 'fallback' ise None döner (Bu durumda GPT devreye girecek).
    """
    if action == "fallback":
        return None

    return INFO_MAP.get(action, "Üzgünüm, şu an sistemsel bir hata var.")
