import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki API key'i yüklüyor

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Merhaba, çalışıyor musun?"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print("Hata:", e)
