import telebot
import openai
import os

# Tokenlarni muhitdan olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Tokenlar bo‘sh emasligini tekshirish
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not found in environment.")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not found in environment.")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Assalomu alaykum! Menga xabar yozing va men tarjima qilib beraman.")

# Har qanday matnga javob berish
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {str(e)}")

# Botni ishga tushirish
if __name__ == "__main__":
    print("🤖 TilmochGPT ishga tushdi...")
    bot.infinity_polling()
