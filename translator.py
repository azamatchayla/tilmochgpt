import openai
import os

# OpenAI API kaliti Render serverdagi muhitdan olinadi
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Matnni GPT orqali avtomatik aniqlanadigan manba tilidan foydalanuvchi tanlagan tilga tarjima qiladi
def translate_text(text, to_lang):
    prompt = f"Please translate the following message to {to_lang.upper()}. Auto-detect the source language:\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Agar kerak bo‘lsa, gpt-3.5-turbo ham ishlaydi
            messages=[
                {"role": "system", "content": "You are a helpful translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        translated = response.choices[0].message["content"].strip()
        return translated
    except Exception as e:
        return f"❌ Tarjimada xatolik: {str(e)}"
