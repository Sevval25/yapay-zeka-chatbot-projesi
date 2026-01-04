# debug_test.py
from step1_preprocessing import preprocess_text
from step2_nlu import predict_intent_bert
from dialog_manager import decide_action
from constants import INFO_MAP


def debug_intent(text):
    """Intent tahminini detaylı göster"""
    print(f"\n{'=' * 70}")
    print(f"📝 Orijinal Metin: {text}")
    print(f"{'=' * 70}")

    # Preprocessing
    processed = preprocess_text(text)
    print(f"🔄 İşlenmiş Metin: {processed}")

    # Intent tahmini
    intent, confidence = predict_intent_bert(processed)
    print(f"\n🎯 Intent: {intent}")
    print(f"📊 Confidence: {confidence:.4f} ({confidence * 100:.2f}%)")

    # Action kararı
    action = decide_action(intent, confidence)
    print(f"⚡ Action: {action}")

    # Kural tabanlı cevap var mı?
    if action in INFO_MAP:
        print(f"✅ Kural Tabanlı Cevap:")
        print(f"   {INFO_MAP[action]}")
    else:
        print(f"❌ Kural Tabanlı Cevap YOK - GPT devreye girecek")

    print(f"{'=' * 70}\n")

    return intent, confidence, action


# Test soruları
test_questions = [
    "İndirim kodum çalışmıyorsa ne yapmalıyım?",
    "Promosyon kodum geçersiz diyor",
    "Kupon kodum hata veriyor",
    "Final satış ürünlerini iade edebilir miyim?",
    "İade politikası nedir?",
    "Siparişimi nasıl takip edebilirim?",
    "Stokta olmayan ürün var mı?",
]

print("🔍 INTENT DEBUG ARACI")
print("=" * 70)

for question in test_questions:
    debug_intent(question)
    input("⏸️  Devam etmek için Enter'a basın...")

print("\n✅ Debug tamamlandı!")
