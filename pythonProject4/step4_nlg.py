from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(user_input: str) -> str:
    prompt = f"""
Sen kibar, resmi ve Türkçe konuşan bir e-ticaret müşteri temsilcisisin.

Kullanıcı sorusu:
"{user_input}"

Kısa, net ve yardımcı bir cevap ver.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Sen bir müşteri destek asistanısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
