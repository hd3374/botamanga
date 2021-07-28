import telebot
from ZScore import ZScore
import pandas as pd
import dataframe_image as dfi
from bot_token import bot_token

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['zscore'])
def ZScore_handler(message):
    chatId = message.chat.id
    
    show_high, show_low = ZScore()

    show_high_styled = show_high.style.background_gradient()
    show_low_styled = show_low.style.background_gradient()

    dfi.export(show_high_styled, "bb_high.png")
    dfi.export(show_low_styled, "bb_low.png")

    with open('bb_high.png', 'rb') as photo:
        bot.send_photo(chatId, photo)

    with open('bb_low.png', 'rb') as photo:
        bot.send_photo(chatId, photo)


    show_high.to_html('temp.html')
    with open('temp.html', 'rb') as file:
        bot.send_document(chatId, file)
    
    show_low.to_html('temp.html')
    with open('temp.html', 'rb') as file:
        bot.send_document(chatId, file)

print('Arriba la bota')
bot.polling()
