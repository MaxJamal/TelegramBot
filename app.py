import telebot
from config import keys, TOKEN
from extensions import FiatConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты цену которой он хочет узнать> \n<имя валюты в которой надо узнать цену первой валюты> \n<количество первой валюты>\n Увидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, f'{text}')

@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Слишком много параметров.')
        elif len(values) < 3:
            raise APIException('Недостаточно параметров.')

        quote, base, amount = values
        total_base = FiatConverter.get_price(quote.lower(), base.lower(), amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. Ошибка сервера:\n{e}')
    else:
        text = f'Цена {amount} {keys[quote.lower()]} в {keys[base.lower()]} - {round(float(total_base), 2) * float(amount)}'
        bot.send_message(message.chat.id, text)
# Чтобы запустить бота, нужно воспользоваться методом polling.

bot.polling(none_stop=True)
# Параметр none_stop=True говорит, что бот должен стараться не прекращать работу при возникновении каких-либо ошибок.
