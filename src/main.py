import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from user_settings import save_user_lang, get_user_lang
from translator import translate_text

# Muhitdan tokenlarni olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN topilmadi (environment variable)")

bot = telebot.TeleBot(BOT_TOKEN)

# Til tanlash tugmalari
def language_selection_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data="to_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="to_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="to_en"),
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

# Til tanlash callback tugmasi
@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
def handle_language_selection(call: CallbackQuery):
    user_id = str(call.from_user.id)
    selected_lang = call.data.split("_")[1]  # 'uz', 'ru', 'en'
    save_user_lang(user_id, selected_lang)
    bot.answer_callback_query(call.id, text="✅ Til tanlandi!")
    bot.send_message(
        call.message.chat.id,
        f"✅ Endi siz uchun tarjimalar *{selected_lang.upper()}* tiliga qilinadi.",
        parse_mode="Markdown"
    )

# Har qanday matnli xabarni tarjima qilish
@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message):
    user_id = str(message.from_user.id)
    user_lang = get_user_lang(user_id)
    to_lang = user_lang.get("to", "uz")
    original = message.text
    translated = translate_text(original, to_lang)
    bot.reply_to(message, f"✍ Tarjima:\n{translated}")

# Botni ishga tushirish
if __name__ == "__main__":
    print("🤖 TilmochGPT ishga tushdi...")
    bot.infinity_polling()
