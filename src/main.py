
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from user_settings import save_user_lang, get_user_lang
from translator import translate_text

# Muhitdan tokenni olish
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Til tanlash klaviaturasi
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
        "👋 Assalomu alaykum! Men TilmochGPT botman.

"
        "🌍 *Dunyo endi sizning tilingizda so‘zlaydi!*

"
        "Iltimos, tarjima tilini tanlang:"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=language_selection_keyboard())

# Til tanlashni saqlash
@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
def handle_language_selection(call: CallbackQuery):
    user_id = str(call.from_user.id)
    selected_lang = call.data.split("_")[1]
    save_user_lang(user_id, selected_lang)
    bot.answer_callback_query(call.id, text="✅ Til tanlandi!")
    bot.send_message(
        call.message.chat.id,
        f"✅ Endi tarjimalar *{selected_lang.upper()}* tiliga qilinadi.",
        parse_mode="Markdown"
    )

# Guruhda reply qilingan xabarga inline tugma
@bot.message_handler(commands=["tarjima"])
def offer_translation_button(message):
    if message.reply_to_message:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✍ Tarjimani ko‘rish", callback_data=f"translate|{message.reply_to_message.message_id}"))
        bot.send_message(
            message.chat.id,
            "Tarjima uchun quyidagi tugmani bosing 👇",
            reply_to_message_id=message.reply_to_message.message_id,
            reply_markup=markup
        )

# Tugmani bosganda tarjimani faqat foydalanuvchiga ko‘rsatish
@bot.callback_query_handler(func=lambda call: call.data.startswith("translate|"))
def show_translation(call: CallbackQuery):
    user_id = str(call.from_user.id)
    chat_id = call.message.chat.id
    message_id = int(call.data.split("|")[1])
    user_lang = get_user_lang(user_id)
    to_lang = user_lang.get("to", "uz")

    try:
        original_msg = bot.forward_message(user_id, chat_id, message_id)
        original_text = original_msg.text or ""
    except Exception:
        original_text = ""

    if not original_text:
        bot.answer_callback_query(call.id, "❌ Matn topilmadi.", show_alert=True)
        return

    translated = translate_text(original_text, to_lang)
    bot.answer_callback_query(call.id, translated, show_alert=True)

# Shaxsiy chatda avtomatik tarjima
@bot.message_handler(func=lambda m: m.chat.type == "private" and m.text)
def handle_private_text(message):
    user_id = str(message.from_user.id)
    user_lang = get_user_lang(user_id)
    to_lang = user_lang.get("to", "uz")
    translated = translate_text(message.text, to_lang)
    bot.reply_to(message, f"✍ Tarjima:\n{translated}")

# Ishga tushirish
if __name__ == "__main__":
    print("🤖 TilmochGPT ishga tushdi...")
    bot.infinity_polling()
