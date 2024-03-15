import telebot
from telebot import types

telegram_bot = telebot.TeleBot('6662860222:AAF9dv2lK6IrowCYYA06EC05Zh3k_0xx1Cs')

@telegram_bot.message_handler(commands=['start'])
def send_welcome_message(message):
    custom_keyboard = types.ReplyKeyboardMarkup(row_width=2)

    main_button = types.KeyboardButton('Main')
    documentation_button = types.KeyboardButton('Documentation')
    airflow_button = types.KeyboardButton('Airflow')
    mlflow_button = types.KeyboardButton('MLflow')
    
    custom_keyboard.add(main_button, documentation_button, airflow_button, mlflow_button)

    telegram_bot.send_message(message.chat.id, "Привет! Я бот. Содержимое какой страницы желаете получить?", reply_markup=custom_keyboard)

if __name__ == '__main__':
    telegram_bot.polling()