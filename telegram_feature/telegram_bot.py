import telebot
from telebot import types

bot = telebot.TeleBot('6662860222:AAF9dv2lK6IrowCYYA06EC05Zh3k_0xx1Cs')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    itembtn1 = types.KeyboardButton('Main')
    itembtn2 = types.KeyboardButton('Documentation')
    itembtn3 = types.KeyboardButton('Airflow')
    itembtn4 = types.KeyboardButton('MLflow')
    
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, "Привет! Я бот. Содержимое какой страницы желаете получить?", reply_markup=markup)

if __name__ == '__main__':
    bot.polling()