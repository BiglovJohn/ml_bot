from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from local_token import SECRET_KEY
from model import bot

updater = Updater(SECRET_KEY)


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Привет {update.effective_user.first_name}!')


# Функция будет вызвана при получении сообщения
def botMessage(update: Update, context: CallbackContext):
    text = update.message.text  # Что нам написал пользователь
    # print(f"Message: {text}")
    reply = bot(text)  # Готовим ответ
    update.message.reply_text(reply)  # Отправляем ответ обратно пользователю


updater.dispatcher.add_handler(
    CommandHandler('hello', hello))  # Конфигурация, при получении команды hello вызвать функцию hello
# Конфигурацию, при получении любого текстового сообщения будет вызвана функция botMessage
updater.dispatcher.add_handler(MessageHandler(Filters.text, botMessage))

updater.start_polling()
updater.idle()
