from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
import io


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message.from_user.id)
    bot.reply_to(message, f'Привет! {message.from_user.first_name}')

def read_news_file():
    with io.open('data.txt', 'r', encoding='utf-8') as file:
        return file.read()

@bot.message_handler(commands=['news'])
def send_message(message):
    text = read_news_file()
    if text != None:
        bot.reply_to(message, f'{text}')
    else:
        bot.reply_to(message, f'Сегодня нет новостей. Вчерашние новости /oldnews')

def read_oldnews_file():
    with io.open('minus.txt', 'r', encoding='utf-8') as file:
        return file.read()

@bot.message_handler(commands=['oldnews'])
def send_message(message):
    text2 = read_oldnews_file()
    bot.reply_to(message, f'{text2}')

# def send_message():
#     now = datetime.now(pytz.timezone('Asia/Bishkek'))
#     print(now)
#     if now.hour == 17 and now.minute == 22:
#         bot.send_message(chat_id='1291450197', text='Привет, это сообщение из бота!')

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2) 
        bot.load_next_step_handlers()								
        bot.infinity_polling()