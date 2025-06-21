import os
from openai import OpenAI

# OpenAI mijozini API kalit bilan yaratish
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Tarjima funksiyasi
def translate_text(text, to_lang):
    prompt = f"Please translate the following message to {to_lang.upper()}. Auto-detect the source language:\n\n{text}"

    try:
        response = client.chat.completions.create(
           model="gpt-4o"
           
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Tarjimada xatolik: {str(e)}"
