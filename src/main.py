import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from user_settings import save_user_lang, get_user_lang
from translator import translate_text

# --- Token ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# --- Doimiylar ---
MAX_MESSAGE_LEN = 4096          # send_message limiti
MAX_ALERT_LEN   = 180           # answer_callback_query limiti (~200)

# --- Til tanlash tugmalari ---
def language_selection_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский",   callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English",   callback_data="lang_en")
    ]])

# --- /start ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "👋 Assalomu alaykum! Men *TilmochGPT* botman.\n\n"
        "🌍 _Dunyo endi sizning tilingizda so‘zlaydi!_\n\n"
        "Iltimos, tarjima tilini tanlang ⤵️",
        reply_markup=language_selection_keyboard()
    )

# --- Til tanlashni saqlash ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def handle_language_selection(call: CallbackQuery):
    lang = call.data.split("_")[1]                 # uz | ru | en
    save_user_lang(call.from_user.id, lang)
    bot.answer_callback_query(call.id, "✅ Til tanlandi!")
    bot.send_message(
        call.message.chat.id,
        f"✅ Endi tarjimalar *{lang.upper()}* tilida beriladi."
    )

# --- /tarjima (reply bilan) ---
@bot.message_handler(commands=["tarjima"])
def offer_translation_button(message):
    if not (message.reply_to_message and message.reply_to_message.text):
        return                                   # reply bo‘lmasa chiqib ketamiz

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "✍ Tarjimani ko‘rish",
        callback_data=f"tr|{message.reply_to_message.message_id}"
    ))

    bot.send_message(
        chat_id=message.chat.id,
        text="👇 Tarjima tayyor, ko‘rish uchun tugmani bosing",
        reply_to_message_id=message.reply_to_message.message_id,
        reply_markup=markup,
        disable_notification=True
    )

    # /tarjima komandasini o‘chirib yuboramiz (ixtiyoriy)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass

# --- Tugmani bosganda tarjimani faqat bosgan foydalanuvchiga ko‘rsatish ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("tr|"))
def show_translation(call: CallbackQuery):
    original_msg = call.message.reply_to_message
    if not original_msg or not original_msg.text:
        bot.answer_callback_query(call.id, "❌ Matn topilmadi.", show_alert=True)
        return

    lang = get_user_lang(call.from_user.id) or "uz"
    translated = translate_text(original_msg.text, lang)[:MAX_ALERT_LEN-3] + "..." \
                 if len(original_msg.text) > MAX_ALERT_LEN else \
                 translate_text(original_msg.text, lang)

    bot.answer_callback_query(call.id, translated, show_alert=True)

# --- Shaxsiy chatda avtomatik tarjima ---
@bot.message_handler(func=lambda m: m.chat.type == "private" and m.text)
def handle_private_text(message):
    lang = get_user_lang(message.from_user.id) or "uz"
    translated = translate_text(message.text, lang)
    if len(translated) > MAX_MESSAGE_LEN:
        translated = translated[:MAX_MESSAGE_LEN-10] + "\n\n✂️ ..."
    bot.reply_to(message, f"✍ Tarjima:\n{translated}")

# --- Botni ishga tushirish ---
if __name__ == "__main__":
    print("🤖 TilmochGPT ishga tushdi...")
    bot.infinity_polling(skip_pending=True)
