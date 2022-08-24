import telebot.types
from telebot import TeleBot
from configs import *
from keyboard import generate_languages
from googletrans import Translator
import sqlite3

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'about', 'help', "view_history", "clear_history"])
def command_start(message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    if message.text == "/start":
        bot.send_message(chat_id,
                         f"Hello {full_name}! I am a bot translator.\n You can translate any text in any language here🙂")
        give_first_language(message)
    elif message.text == "/about":
        bot.send_message(chat_id, "We did not add any information about ourselves yet")

    elif message.text == "/help":
        bot.send_message(chat_id, "You can chat with the creator of tis bot about the issues => https://t.me/User65031")
    elif message.text == "/view_history":
        view_history(message)
    elif message.text == "/clear_history":
        msg = bot.send_message(chat_id, "Are you sure you want to clear your history? Yes/No",
                               reply_markup=answer())
        bot.register_next_step_handler(msg, clear_history)

    # history(message)
    # msg = bot.send_message(chat_id, "Do you want to clear your history??? Yes/No", reply_markup=answer())
    # bot.register_next_step_handler(msg, clear_history)


def give_first_language(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Choose the first language you want to translate to1️⃣",
                           reply_markup=generate_languages())
    bot.register_next_step_handler(msg, give_second_language)
    #
    # for lang in LANGUAGES.values():
    #     if src != lang:
    #         bot.send_message(chat_id, "Invalid language!!! Enter again!")
    #         give_first_language(message)
    #     else:


def give_second_language(message):
    chat_id = message.chat.id
    src = message.text
    bot.send_message(chat_id, f"You have chosen {src} language")
    msg = bot.send_message(chat_id, "Choose the second language you want to translate2️⃣",
                           reply_markup=generate_languages())
    bot.register_next_step_handler(msg, give_text, src)

    #
    # for lang in LANGUAGES.values():
    #     if dest != lang:
    #         bot.send_message(chat_id, "Invalid language!!! Enter again!")
    #         give_second_language(message)
    #     else:


def give_text(message, src):
    chat_id = message.chat.id
    dest = message.text
    bot.send_message(chat_id, f"You have chosen {dest} ")
    msg = bot.send_message(chat_id, "Enter the text you want to translate📝")
    bot.register_next_step_handler(msg, translate, src, dest)


def translate(message, src, dest):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    text = message.text
    translator = Translator()
    translated_text = translator.translate(src=src, dest=dest, text=text).text
    bot.send_message(chat_id, translated_text)
    msg = bot.send_message(chat_id, "Do you want to enter text again ? Yes/No", reply_markup=answer())
    bot.register_next_step_handler(msg, translate_again)

    database = sqlite3.connect("users.db")
    cursor = database.cursor()
    cursor.execute(
        """INSERT INTO history(telegram_id, full_name, first_lang, second_lang, original_text, translated_text) VALUES 
        (?, ?, ?, ?, ?, ?)
        """, (chat_id, full_name, src, dest, text, translated_text))
    database.commit()
    database.close()


def translate_again(message):
    text = message.text
    if text == "Yes":
        give_first_language(message)
    else:
        commands(message)


def view_history(message):
    chat_id = message.chat.id

    database = sqlite3.connect("users.db")
    cursor = database.cursor()
    msg = bot.send_message(chat_id, "Your history of activity", reply_markup=back())
    bot.register_next_step_handler(msg, back_function)
    cursor.execute(
        """SELECT telegram_id, full_name, first_lang, second_lang, original_text, translated_text FROM history 
        WHERE telegram_id = ?""", (chat_id,))
    for item in cursor:
        items = f"Telegram Id = {item[0]}\nFullname = {item[1]}\nFirst Language = {item[2]}\nSecond Language = {item[3]}" \
                f"\nOriginal text = {item[4]}\nTranslated text = {item[5]}"
        bot.send_message(chat_id, items)

    database.close()


def clear_history(message):
    chat_id = message.chat.id
    text = message.text
    if text == "Yes":
        database = sqlite3.connect("users.db")
        cursor = database.cursor()
        cursor.execute("DELETE FROM history WHERE telegram_id = ?", (chat_id,))
        msg = bot.send_message(chat_id, "Your history has been cleared🗑️!!!", reply_markup=back())
        bot.register_next_step_handler(msg, back_function)
        database.commit()
        database.close()
    else:
        commands(message)


# ===============================================================================================================================

answers = ['Yes', "No"]


def answer():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for ans in answers:
        btn = telebot.types.KeyboardButton(text=ans)
        buttons.append(btn)
    markup.add(*buttons)
    return markup


def back():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton(text="🔙 back")
    markup.add(btn)
    return markup


def back_function(message):
    chat_id = message.chat.id
    text = message.text
    if text == "🔙 back":
        commands(message)


def commands(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Here are all the commands\n"
                              "/start -- to translate\n"
                              "/about -- about us\n"
                              "/help -- ask for help\n"
                              "/view_history -- Your activity history\n"
                              "/clear_history -- clear your activity history🧹")


bot.polling(none_stop=True)
