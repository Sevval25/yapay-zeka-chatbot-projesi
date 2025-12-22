import streamlit as st
from step2_nlu import predict_intent_bert
from dialog_manager import decide_action
from step4_nlg import generate_response
from step5_logging import log_conversation

# Sayfa Ayarları
st.set_page_config(page_title="Müşteri Destek Asistanı", page_icon="🤖")

# 🔹 KURAL TABANLI SABİT CEVAPLAR
INFO_MAP = {
    "get_shipping_info": "Kargo süremiz 2–4 iş günü arasındadır.",
    "get_discount_info": "İndirimli ürünlerimizi web sitemizden inceleyebilirsiniz.",
    "get_campaign_info": "Güncel kampanyalarımız ana sayfamızda yer almaktadır.",
    "get_price_info": "Ürün fiyat bilgileri ürün sayfasında yer almaktadır.",
    "get_availability_info": "Stok durumu ürün sayfasında görüntülenmektedir.",
    "support": "Destek ekibimiz size yardımcı olmaktan memnuniyet duyar."
}

# 🔹 Yardımcı Fonksiyonlar
def rewrite_with_gpt(base_text, user_text):
    prompt = f"Kullanıcı şunu sordu: '{user_text}'. Aşağıdaki cevabı nazik ve doğal bir şekilde ilet: '{base_text}'"
    return generate_response(prompt)

def fallback_with_gpt(user_text):
    prompt = f"Kullanıcı mesajı: '{user_text}'. Nazikçe selam ver veya yardım teklif et."
    return generate_response(prompt)

# --- ARAYÜZ ---
st.title("🤖 Akıllı Destek Asistanı")
st.markdown("Sorularınızı aşağıya yazabilirsiniz.")

# Sohbet Geçmişi (Streamlit'te mesajların kalması için)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
user_input = st.chat_input("Mesajınızı buraya yazın...")

if user_input:
    # 1. Kullanıcı mesajını göster
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. İşleme (Backend Mantığın)
    with st.spinner("Düşünüyorum..."):
        # Intent + confidence
        intent, confidence = predict_intent_bert(user_input)
        
        # Karar
        action = decide_action(intent, confidence)

        # Yanıt üretimi
        if action in INFO_MAP:
            base_response = INFO_MAP[action]
            response = rewrite_with_gpt(base_response, user_input)
        else:
            response = fallback_with_gpt(user_input)

    # 3. Yanıtı Göster
    with st.chat_message("assistant"):
        st.markdown(response)
        # İstersen güven skorunu küçük bir not olarak ekleyebilirsin:
        st.caption(f"Intent: {intent} (%{int(confidence*100)})")

    # 4. Geçmişe ve Loglara ekle
    st.session_state.messages.append({"role": "assistant", "content": response})
    log_conversation(user_input, response)
