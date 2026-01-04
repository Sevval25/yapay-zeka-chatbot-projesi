from flask import Flask, request, jsonify
from flask_cors import CORS

# Diğer modüllerimiz
from step1_preprocessing import preprocess_text
from step2_nlu import predict_intent_bert
from dialog_manager import decide_action
from step4_nlg import generate_response
from step5_logging import log_conversation
from constants import INFO_MAP

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False


def fallback_with_gpt(user_text):
    """
    Model emin olamadığında (Fallback) veya selamlaşma gibi durumlarda
    GPT devreye girer.
    """
    system_prompt = """
    Sen kibar, profesyonel ve Türkçe konuşan bir e-ticaret müşteri temsilcisisin.

    Görevin:
    1. Kullanıcının sorusuna kısa, doğal ve yardımsever bir yanıt ver.
    2. Eğer konu teknik bir işlemse (sipariş iptali, iade süreci vb.) detaylara girmeden "Müşteri hizmetlerimizle iletişime geçebilirsiniz" de.
    3. Selamlaşmalara (Merhaba, nasılsın) samimi karşılık ver.

    Cevabın maksimum 2-3 cümle olsun.
    """

    # step4_nlg.py içindeki güncellediğimiz fonksiyona gönderiyoruz
    return generate_response(system_prompt, user_text)


@app.route("/chat", methods=["POST"])
def chat():
    # 1. Kullanıcıdan veriyi al
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Lütfen boş bir mesaj göndermeyin."})

    # 2. Önişleme ve NLU (BERT + Kurallar)
    processed_input = preprocess_text(user_input)
    intent, confidence = predict_intent_bert(processed_input)

    # intent burada artık "product_stock", "return_cancel" gibi yeni isimlerinle geliyor.

    # 3. Karar Mekanizması (Güven skoru kontrolü)
    action = decide_action(intent, confidence)

    # DEBUG: Terminalde ne olup bittiğini gör
    print(f"🔍 DEBUG: Girdi='{user_input}' -> Intent='{intent}' ({confidence:.2f}) -> Action='{action}'")

    # 4. Yanıt Üretimi
    response = ""
    source = ""

    if action == "fallback":
        # BERT emin değilse veya kural yoksa -> GPT
        print("🤖 Rota: GPT (Fallback)")
        response = fallback_with_gpt(user_input)
        source = "gpt_fallback"

    elif action in INFO_MAP:
        # BERT emin ve INFO_MAP içinde bu etiket var -> Hazır Cevap
        # Örneğin action="product_stock" ise INFO_MAP["product_stock"] çalışır.
        print(f"rule Rota: Kural Tabanlı ({action})")
        response = INFO_MAP[action]
        source = "rule_based"

    else:
        # Beklenmedik bir hata durumu
        response = "Üzgünüm, şu an sistemde geçici bir sorun var. Lütfen daha sonra tekrar deneyin."
        source = "error"

    # 5. Loglama (Konuşma geçmişini kaydet)
    log_conversation(user_input, response, intent, confidence)

    # 6. Sonucu döndür
    return jsonify({
        "intent": intent,
        "confidence": round(confidence, 2),
        "action": action,
        "source": source,
        "response": response
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "active"})


if __name__ == "__main__":
    print("🚀 Chatbot Sunucusu Başlatılıyor...")
    print("✅ Constants, NLU ve Data uyumu: TAMAM (product_stock, return_cancel v2)")
    app.run(debug=True, port=5000)
