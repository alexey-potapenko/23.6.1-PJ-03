import telebot

from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    print('start')
    text = "Чтобы начать работу введите команду боту в следующем формате : \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def velues(message:telebot.types.Message):
    text = "доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('слишком много параметров')

        base, quote, amount = values  # fsym = Имя валюты которую хотим продать, tsyms = список валют, в которых надо узнать стоимость fsym, amount = количество fsym
        total_base = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {base} в {quote} = {total_base}'
        bot.send_message(message.chat.id, text)













# bot.polling(none_stop=True) # Запуск бота
bot.polling() # Запуск бота