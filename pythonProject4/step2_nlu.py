import torch
import torch.nn.functional as F
from transformers import BertTokenizerFast, BertForSequenceClassification
from step1_preprocessing import preprocess_text
from constants import ID2LABEL

MODEL_PATH = "models/bert_intent"

# --- KURAL TABANLI MÜDAHALE (SIRALI VE DÜZENLİ) ---
# constants.py içindeki ID2LABEL sırasına (0->5) göre düzenlenmiştir.
KEYWORD_RULES = {
    # --- ID: 0 -> shipping (Kargo) ---
    "kargo": "shipping",
    "takip": "shipping",
    "teslimat": "shipping",
    "paket": "shipping",
    "nerede": "shipping",

    # --- ID: 1 -> discount_campaign (İndirim ve Kampanya) ---
    "indirim": "discount_campaign",
    "kupon": "discount_campaign",
    "kampanya": "discount_campaign",
    "kod": "discount_campaign",
    "promosyon": "discount_campaign",

    # --- ID: 2 -> product_stock (Stok ve Ürün) ---
    "stok": "product_stock",
    "tükenmiş": "product_stock",
    "gelecek": "product_stock",
    "ön sipariş": "product_stock",
    "temin": "product_stock",
    "ayırt": "product_stock",

    # --- ID: 3 -> account_payment (Hesap ve Ödeme) ---
    "hesap": "account_payment",
    "ödeme": "account_payment",
    "fatura": "account_payment",
    "şifre": "account_payment",
    "üye": "account_payment",
    "giriş": "account_payment",

    # --- ID: 4 -> return_cancel (İade ve İptal) ---
    "iptal": "return_cancel",
    "iade": "return_cancel",
    "değişim": "return_cancel",
    "vazgeçtim": "return_cancel",
    "geri gönder": "return_cancel",

    # --- ID: 5 -> customer_support (Müşteri Hizmetleri) ---
    "canlı": "customer_support",
    "destek": "customer_support",
    "temsilci": "customer_support",
    "iletişim": "customer_support"
}

print("🔄 Model yükleniyor...")
try:
    tokenizer = BertTokenizerFast.from_pretrained(MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    print("✅ Model başarıyla yüklendi!")
except Exception as e:
    print(f"⚠️ UYARI: Model yüklenemedi. Önce 'python train_intent.py' çalıştırın. Hata: {e}")
    model = None
    tokenizer = None


def predict_intent_bert(text: str):
    """
    1. Önce KURAL (Keyword) kontrolü yap.
    2. Kural yoksa BERT ile tahmin et.
    """
    clean_text = preprocess_text(text)

    if not clean_text:
        return "fallback", 0.0

    # --- ADIM 1: Kural Kontrolü ---
    for keyword, intent_name in KEYWORD_RULES.items():
        if keyword in clean_text:
            print(f"⚡ KURAL ÇALIŞTI: '{keyword}' bulundu -> '{intent_name}' seçildi.")
            return intent_name, 1.0

    # --- ADIM 2: BERT Tahmini ---
    if model is None:
        return "fallback", 0.0

    inputs = tokenizer(
        clean_text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(outputs.logits, dim=1)
    confidence, predicted_id = torch.max(probs, dim=1)

    confidence = float(confidence.item())
    predicted_id = int(predicted_id.item())

    # ID'yi isme çevir (constants.py referans alınarak)
    if predicted_id in ID2LABEL:
        intent = ID2LABEL[predicted_id]
    else:
        intent = "fallback"

    print(f"🔍 BERT: text='{text}' -> intent='{intent}', confidence={confidence:.4f}")

    return intent, confidence
