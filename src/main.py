import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Tokenni xavfsiz olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Til tanlash keyboardi
def language_selection_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data="to_uz"),
            InlineKeyboardButton("🇷🇺 Ruscha", callback_data="to_ru"),
            InlineKeyboardButton("🇬🇧 Inglizcha", callback_data="to_en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        "👋 Assalomu alaykum! Men TilmochGPT botman.\n\n"
        "🌍 *Dunyo siz uchun qaysi tilda so‘zlasin?*\n\n"
        "Iltimos, tarjima natijalarini ko‘rmoqchi bo‘lgan tilni tanlang:"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=language_selection_keyboard()
    )

# Til tanlash callback
@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
def handle_language_selection(call: CallbackQuery):
    user_id = str(call.from_user.id)
    selected_lang = call.data.split("_")[1]  # 'uz', 'ru', 'en'
    bot.answer_callback_query(call.id, text="✅ Til tanlandi!")
    bot.send_message(
        call.message.chat.id,
        f"✅ Endi siz uchun tarjimalar *{selected_lang.upper()}* tiliga qilinadi.",
        parse_mode="Markdown"
    )

# Ishga tushirish
if __name__ == "__main__":
    print("🤖 TilmochGPT ishga tushdi...")
    bot.infinity_polling()

