from flask import Flask, request, jsonify
from flask_cors import CORS

from step2_nlu import predict_intent_bert
from dialog_manager import decide_action
from step4_nlg import generate_response
from step5_logging import log_conversation

app = Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False

# 🔹 KURAL TABANLI SABİT CEVAPLAR
INFO_MAP = {
    "get_shipping_info": "Kargo süremiz 2–4 iş günü arasındadır.",
    "get_discount_info": "İndirimli ürünlerimizi web sitemizden inceleyebilirsiniz.",
    "get_campaign_info": "Güncel kampanyalarımız ana sayfamızda yer almaktadır.",
    "get_price_info": "Ürün fiyat bilgileri ürün sayfasında yer almaktadır.",
    "get_availability_info": "Stok durumu ürün sayfasında görüntülenmektedir.",
    "support": "Destek ekibimiz size yardımcı olmaktan memnuniyet duyar."
}

# 🔹 Sabit cevabı GPT ile sadece güzelleştirme
def rewrite_with_gpt(base_text, user_text):
    prompt = f"""
Kullanıcı şu soruyu sordu:
"{user_text}"

Aşağıdaki cevabı kullanıcıya doğal ve nazik şekilde ilet.
"{base_text}"
"""
    return generate_response(prompt)

# 🔹 Belirsiz sorular için fallback GPT
def fallback_with_gpt(user_text):
    prompt = f"""
Kullanıcı şu mesajı gönderdi:
"{user_text}"

Eğer soru belirsizse nazikçe yardım teklif et,
eğer selamlaşmaysa kısa bir karşılama yap.
"""
    return generate_response(prompt)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"response": "Mesaj boş olamaz."})

    # 1️⃣ Intent + confidence
    intent, confidence = predict_intent_bert(user_input)

    # 2️⃣ Karar
    action = decide_action(intent, confidence)

    # 3️⃣ Yanıt üretimi
    if action in INFO_MAP:
        base_response = INFO_MAP[action]
        response = rewrite_with_gpt(base_response, user_input)
        source = "rule + gpt"
    else:
        response = fallback_with_gpt(user_input)
        source = "gpt"

    # 4️⃣ Log
    log_conversation(user_input, response)

    return jsonify({
        "intent": intent,
        "confidence": round(confidence, 2),
        "source": source,
        "response": response
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("🚀 Chatbot çalışıyor...")
    app.run(debug=True)
