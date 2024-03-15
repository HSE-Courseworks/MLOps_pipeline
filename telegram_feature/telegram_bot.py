import telebot

bot = telebot.TeleBot('6662860222:AAF9dv2lK6IrowCYYA06EC05Zh3k_0xx1Cs')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот. Как я могу помочь?")

if __name__ == '__main__':
    bot.polling()