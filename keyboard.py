from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES


def generate_languages():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []
    for lang in LANGUAGES.values():
        btn = KeyboardButton(text=lang)
        buttons.append(btn)
    markup.add(*buttons)
    return markup
