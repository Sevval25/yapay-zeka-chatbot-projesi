from openai import OpenAI
import os
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("⚠️ UYARI: OPENAI_API_KEY bulunamadı. .env dosyasını kontrol et.")

client = OpenAI(api_key=api_key)

def generate_response(system_instruction: str, user_input: str) -> str:
    """
    GPT-4o-mini kullanarak yanıt üretir.
    system_instruction: Botun nasıl davranacağı (Sen bir asistansın vs.)
    user_input: Kullanıcının mesajı
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # veya gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ GPT Hatası: {e}")
        return "Üzgünüm, şu an bağlantı sorunu yaşıyorum. Lütfen daha sonra tekrar deneyin."
